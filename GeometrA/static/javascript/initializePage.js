$(document).ready(function() {
    function callback(result) {
        ToolBar();
        NodeTree();
        Screen(document.getElementById('Screen'));
        if (result == 'exist') {
            Log();
        }
        else {
            InitializePage()
        }
    }
    Get('/GeometrA/checkLog', callback)
})

function InitializePage() {
    swal({
        title: 'Welcome to GeometrA',
        text: "Please load a project or create a new one",
        type: 'info',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Load',
        cancelButtonText: 'Create',
        buttonsStyling: true,
        allowEscapeKey: false,
        allowOutsideClick: false,
    }).then((result) => {
        if (result.value) {
            Load()
        } else if (result.dismiss === 'cancel') {
            Create()
        }
    })
}

function Log() {
    Get('/GeometrA/log', function (result) {
        if (result == 'Success') {
            WorkSpace();
        }
        else {
            InitializePage()
        }
    });
}
