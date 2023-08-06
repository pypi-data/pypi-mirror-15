var grid = Ext.getCmp('{{ component.grid.client_id }}');
var exportUrl = '{{ component.url_export }}';

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

function importTemplate() {
    var record = getSelectedRecord();
    if (record) {

    }
}


function exportTemplate() {
    var record = getSelectedRecord();
    if (record) {
        var request = {
            url: exportUrl,
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


function getSelectedRecord() {
    var sm = grid.getSelectionModel();
    if (sm.hasSelection()) {
        return sm.getSelected();
    }

    return showWarning('Не выбрана запись!');
}