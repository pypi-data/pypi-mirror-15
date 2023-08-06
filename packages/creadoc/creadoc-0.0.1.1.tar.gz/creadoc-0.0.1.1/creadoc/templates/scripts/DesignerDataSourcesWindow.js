var gridSource = Ext.getCmp('{{ component.source_grid.client_id }}');
var gridDestination = Ext.getCmp('{{ component.destination_grid.client_id }}');


var urlSave = '{{ component.save_url | safe }}';


/**
 * Подключение выбранного источника данных к шаблону
 */
function plugSource() {
    var record = getSelectedRecords(gridSource);

    if (record) {
        moveRecordsToOtherGrid(record, gridSource, gridDestination);
    }
}


/**
 * Отключение выбранного источника данных от шаблона
 */
function unplugSource() {
    var record = getSelectedRecords(gridDestination);

    if (record) {
        moveRecordsToOtherGrid(record, gridDestination, gridSource);
    }
}


/**
 * Получение текущей выделенной записи из указанного грида
 * В случае, если запись не выделена - выводим окно с предупреждением
 */
function getSelectedRecords(grid) {
    var selectionModel = grid.getSelectionModel();

    if (selectionModel.hasSelection()) {
        return selectionModel.getSelections();
    } else {
        showWarning('Не выбрана запись!', 'Внимание!');
    }
}


/**
 * Перенос указанных записей из sourceGrid в destinationGrid
 */
function moveRecordsToOtherGrid(records, sourceGrid, destinationGrid) {
    Ext.iterate(records, function(record) {
        var newRecord = new Ext.data.Record(record.data);

        destinationGrid.getStore().add(newRecord);
        sourceGrid.getStore().remove(record);
    });

    win.changesCount += 1
}


/**
 * Отправка запроса на сохранение изменений в списке источников данных
 */
function saveSources() {
    var mask = new Ext.LoadMask(win.body);
    mask.show();

    var rows = [];
    var fullRows = [];
    gridDestination.getStore().each(function(row) {
        rows.push(row.get('id'));
        fullRows.push([
            row.get('id'),
            row.get('name'),
            row.get('url')
        ])
    });

    var request = {
        'url': urlSave,
        'params': {
            'rows': Ext.encode(rows),
            'report_id': win.actionContextJson['report_id']
        },
        'success': function(response) {
            // По окончанию сохранения отправляем событие во фрейм
            var result = win.fireEvent('afterSaveSources', fullRows);

            if (result) {
                mask.hide();
                win.close(true);
            }
        },
        'failure': function() {
            mask.hide();
            uiAjaxFailMessage.apply(this, arguments);
        }
    };

    Ext.Ajax.request(request);
}


/**
 * Закрытие окна
 */
function closeWindow() {
    win.close();
}