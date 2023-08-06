var grid = Ext.getCmp('{{ component.grid.client_id }}');

grid.on('aftereditrequest', refreshStoreHandler);
grid.on('afternewrequest', refreshStoreHandler);


/**
 * Обновление стора грида после закрытия окна создания/редактирование записи
 */
function refreshStoreHandler(cmp, response, request) {
    var editWin = smart_eval(response.responseText);

    if (editWin) {
        editWin.on('close', function() {
            grid.refreshStore();
        });
    }

    return false;
}


/**
 * Функция загрузки шаблона
 */
function importTemplate() {
    var request = {
        url: '{{ component.url_import }}',
        success: function(response) {
            var importWin = smart_eval(response.responseText);
            importWin.on('close', function() {
                grid.refreshStore();
            });
        },
        failure: function() {
            uiAjaxFailMessage.apply(this, arguments);
        }
    };

    Ext.Ajax.request(request);
}


/**
 * Функция выгрузки шаблона
 */
function exportTemplate() {
    var record = getSelectedRecord();
    if (record) {
        var request = {
            url: '{{ component.url_export }}',
            params: {'report_id': record.get('id')},
            success: function(response) {
                smart_eval(response.responseText);
            },
            failure: function() {
                uiAjaxFailMessage.apply(this, arguments);
            }
        };

        Ext.Ajax.request(request);
    }
}


/**
 * Получение записи по текущей выделенной записи грида
 */
function getSelectedRecord() {
    var sm = grid.getSelectionModel();
    if (sm.hasSelection()) {
        return sm.getSelected();
    }

    return showWarning('Не выбрана запись!');
}