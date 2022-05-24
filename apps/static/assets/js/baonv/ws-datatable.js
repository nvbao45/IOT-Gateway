$("#datatable").DataTable({
    serverSide: true,
    ajax: {
        url: '/ws/data',
        type: 'POST',
    },
    searching: false,
    ordering: false,
    columns: [
        { "data": "node_id", "sortable": false },
        { "data": "node_name" },
        { "data": "sensor" },
        { "data": "value" },
        { "data": "timestamp" },
        { "data": "gateway_id" },
    ],
})