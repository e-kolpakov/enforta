/*global $*/
$.extend(true, $.fn.dataTable.defaults, {
    "oLanguage": {
        "sProcessing": "Загрузка...",
        "sLengthMenu": "Показать _MENU_ записей",
        "sZeroRecords": "Записи отсутствуют.",
        "sInfo": "Записи с _START_ по _END_ из _TOTAL_ записей",
        "sInfoEmpty": "Записи с 0 до 0 из 0 записей",
        "sInfoFiltered": "(отфильтровано из _MAX_ записей)",
        "sInfoPostFix": "",
        "sSearch": "Быстрый поиск:",
        "sUrl": "",
        "oPaginate": {
            "sFirst": "Первая",
            "sPrevious": "Предыдущая",
            "sNext": "Следующая",
            "sLast": "Последняя"
        },
        "oAria": {
            "sSortAscending": ": активировать для сортировки столбца по возрастанию",
            "sSortDescending": ": активировать для сортировки столбцов по убыванию"
        },
        sEmptyTable: "Нет записей для отображения"
    }
});