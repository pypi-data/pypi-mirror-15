var iframe = Ext.get('creadoc-iframe');
var iframeWindow = iframe.dom.contentWindow;
// Текущий идентификатор шаблона
var reportId = Ext.decode('{{ component.report_id }}');

// url для сохранения шаблона
var reportSaveUrl = '{{ component.save_report_url }}';
// url для снятия блокировки с шаблона
var reportReleaseUrl = '{{ component.release_report_url }}';
// url для открытия окна со списком доступных и подключенных источников данных
var reportSourcesWindowUrl = '{{ component.sources_window_url }}';


var autoSaver;
// Промежуток в миллисекундах между запусками процедуры автосохранения
var autoSaveTimeOut = Ext.decode('{{ component.autosave_timeout }}');


win.on('show', function() {
    // Инициализация автосохранения
    autoSaver = new AutoSaver(autoSaveTimeOut).run();
});


// Код клавиши "S"
var CharCodeS = 19;

// Сохранение шаблона при использовании комбинации клавиш ctrl + S
iframeWindow.addEventListener('keydown', function(e) {
    if (e.ctrlKey || e.metaKey) {
        e.preventDefault();

        if (e.charCode == CharCodeS) {
            saveTemplate();
        }
    }
});


/**
 * Проверка является ли текущий шаблон новым и еще не сохраненным
 * @returns {boolean}
 */
function isNewReport() {
    return reportId == 0;
}


/**
 * Формирование объекта события
 * @returns {CustomEvent}
 */
function getTemplateEvent(callback) {
    return new CustomEvent(
        'getTemplate', {
            bubbles : true,
            cancelable : true,
            detail: {'callback': callback}
        }
    );
}


/**
 * Формирование события на обновление списка источников данных
 * @param rows
 * @returns {CustomEvent}
 */
function getDataSourceEvent(rows) {
    return new CustomEvent('refreshSources', {
        bubbles : true,
        cancelable : true,
        detail: {'rows': rows}
    });
}


/**
 * Обработка диалога подтверждения закрытия окна
 * @returns {boolean}
 */
function closeWindow() {
    Ext.Msg.confirm(
        'Внимание!',
        'Все несохраненные изменения будут утеряны. Закрыть окно?',
        function(result) {
            if (result == 'yes') {
                requestReleaseReport(function() {
                    win.close(true);
                });
                // При успешном закрытии окна очищаем сессию из кэша
                autoSaver.removeSession();
            }
        }
    );

    return false;
}


/**
 * Отправка запроса на освобождение мьютекса
 * @param callback Функция, вызываемая по окончанию запроса
 * @param rId Идентификатор отчета.
 *  В случае отсутствия берется идентификатор открытого в данный момент отчета.
 */
function requestReleaseReport(callback, rId) {
    var request = {
        'url': reportReleaseUrl,
        'params': {
            'report_id': rId !== undefined ? rId : reportId
        },
        success: callback,
        failure: function() {
            uiAjaxFailMessage.apply(this, arguments);
        }
    };

    Ext.Ajax.request(request);
}


/**
 * Отправка запроса на сохранение шаблона
 * @param id
 * @param reportName
 * @param template
 */
function saveRequest(id, reportName, template) {
    var mask = new Ext.LoadMask(win.body, {msg: 'Сохранение...'});
    mask.show();

    var request = {
        url: reportSaveUrl,
        params: {
            'id': id || 0,
            'name': reportName || '',
            'report': template
        },
        success: function(response) {
            mask.hide();
            var result = Ext.decode(response.responseText);

            if (result['success'] && result['report_id']) {
                reportId = result['report_id'];
            }

            win.fireEvent('afterSaveReport', reportId, reportName, template);
        },
        failure: function() {
            mask.hide();
            uiAjaxFailMessage.apply(this, arguments);
        }
    };

    Ext.Ajax.request(request);
}


/**
 * Обертка над сохранением шаблона. Перед сохранением посылает событие на получение объекта шаблона.
 * @param reportId Идентификатор шаблона
 * @param reportName Наименование шаблона
 */
function saveRequestWrapper(reportId, reportName) {
    iframeWindow.dispatchEvent(getTemplateEvent(function(template) {
        saveRequest(reportId, reportName, template);
    }));
}


/**
 * Сохранение шаблона
 */
function saveTemplate() {
    if (isNewReport()) {
        showNameChangeDialog(function(name) {
            saveRequestWrapper(reportId, name, true);
        });
    } else {
        saveRequestWrapper(reportId, '');
    }
}


/**
 * Сохранение шаблона под новым наименованием
 */
function saveTemplateAs() {
    showNameChangeDialog(function(name) {
        // Освобождаем предыдущий шаблон перед тем,
        // как сохранить его под новым именем.
        requestReleaseReport(function() {
            saveRequestWrapper(0, name, true);
        });
    });
}


/**
 * Диалоговое окно с вводом наименования шаблона
 * @param callback Функция обратного вызова, срабатывающая после ввода наименования.
 *  На вход первым параметром получает введенное наименование.
 * @param message Кастомное сообщение в окне ввода наименования шаблона
 * @param declineCallback Функция, срабатывающая при отказе от ввода наименования
 */
function showNameChangeDialog(callback, message, declineCallback) {
    if (!message) {
        message = 'Введите наименование шаблона';
    }

    Ext.Msg.prompt(
        'Сохранение шаблона',
        message,
        function(result, name) {
            if (result == 'ok' && name) {
                callback(name);
            } else {
                declineCallback();
            }
        }
    );
}


/**
 * Отображение окна со списком доступных и подключенных источников данных
 */
function openDataSourceWindow() {
    // Чтобы привязать источник данных к шаблону нам нужно его вначале сохранить
    if (isNewReport()) {
        var message = 'Для подключения источника данных сначала требуется сохранить шаблон.' +
            '<br> Введите наименование шаблона.';

        showNameChangeDialog(function(name) {
            saveRequestWrapper(reportId, name);
        }, message);

        // При получении события об окончании сохранения шаблона
        // формируем запрос на получение окна со списком источников
        win.on('afterSaveReport', openDataSourceWindowRequest, win, {'single': true});
    } else {
        openDataSourceWindowRequest(reportId);
    }
}

/**
 * Запрос на формирование окна
 */
function openDataSourceWindowRequest(reportId) {
    var request = {
        url: reportSourcesWindowUrl,
        params: {'report_id': reportId},
        success: function(response) {
            var editWindow = smart_eval(response.responseText);
            editWindow.on('afterSaveSources', function(rows) {
                iframeWindow.dispatchEvent(getDataSourceEvent(rows));
                return true;
            });
        },
        failure: function() {
            uiAjaxFailMessage.apply(this, arguments);
        }
    };

    Ext.Ajax.request(request);
}


/**
 * Автосохранение шаблона в локальном кэше
 * @param timeout Интервал между вызовами процедуры сохранения
 */
function AutoSaver(timeout) {
    var intervalId;
    var self = this;
    var sessionKey = 'creadoc_designer_session';
    var reportIdKey = 'report_id';

    self.timeout = timeout;
    self.storage = window.localStorage;

    // Фэлбэк на случай отсутствия поддержки локального хранилища
    if (!self.storage) {
        return {
            'getTemplate': Ext.emptyFn,
            'hasPreviousSession': Ext.emptyFn,
            'createSession': Ext.emptyFn,
            'updateSession': Ext.emptyFn,
            'removeSession': Ext.emptyFn,
            'run': Ext.emptyFn
        }
    }

    /**
     * Запращивает у дизайнера текущее состояния шаблона и
     * передает его в указанную первым аргументом функцию
     * @param callback Функция обратного вызова, получает на вход объект шаблона
     */
    self.getTemplate = function(callback) {
        iframeWindow.dispatchEvent(getTemplateEvent(callback));
    };

    /**
     * Проверка наличия незавершенной сессии
     * @returns {boolean}
     */
    self.hasPreviousSession = function() {
        return !!self.storage.getItem(sessionKey);
    };

    /**
     * Создание новой сессии
     */
    self.createSession = function() {
        self.getTemplate(function(template) {
            self.storage.setItem(sessionKey, template);
            self.storage.setItem(reportIdKey, reportId);
        });
    };

    /**
     * Обновление сессии
     */
    self.updateSession = function() {
        self.createSession();
    };

    /**
     * Удаление сессии
     */
    self.removeSession = function() {
        self.storage.removeItem(sessionKey);
        self.storage.removeItem(reportIdKey);

        intervalId ? window.clearInterval(intervalId) : null;
    };

    /**
     * Перезапуск сессии
     */
    self.reloadSession = function() {
        self.removeSession();
        self.run();
    };

    /**
     * Запуск логики автосохранения
     */
    self.run = function() {
        // Если предыдущей сессии не найдено, то просто создаем и запускаем новую
        if (!self.hasPreviousSession()) {
            self.createSession();

            intervalId = window.setInterval(function() {
                self.updateSession();
            }, self.timeout);
        } else {
            Ext.Msg.confirm(
                'Внимание!',
                'Предыдущая сессия была некорректно завершена!<br>' +
                'Вы можете сохранить предыдущую сессию как отдельный шаблон, ' +
                'чтобы продолжить его редактирование позднее.<br>' +
                'В случае отказа от сохранения данные предыдущей сессии будут удалены.<br>' +
                'Вы хотите сохранить предыдущую сессию как новый шаблон?',
                function(result) {
                    if (result == 'yes') {
                        var rId = self.storage.getItem(reportIdKey);
                        var template = self.storage.getItem(sessionKey);

                        // Сохранение отчета
                        showNameChangeDialog(function(name) {
                            saveRequest(0, name, template);

                            // Если в сессии висит уже сохраненный ранее шаблон,
                            // то нам нужно освободить его от мьютекса
                            if (rId && rId > 0) {
                                requestReleaseReport(Ext.emptyFn, rId);
                            }
                        }, false, function() {
                            // Если пользователь отказался ввести наименование отчета,
                            // то сам дурак. Удаляем данные сессии.
                            self.reloadSession();
                        });
                    }

                    // После сохранения отчета
                    // сбрасываем предыдущую сессию и перезапускаем ее
                    self.reloadSession();
                }
            );
        }

        return self;
    }
}