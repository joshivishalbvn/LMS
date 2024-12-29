

$(document).on('click', '.delete-btn', function (e) {
    var id = $(this).data("id")
    var name = $(this).data("title")
    if (name == "None") {
        name = ""
    }
    var url = $(this).data("url")

    Swal.fire({
        html: `Are you sure you want to delete <b>${name}</b> ?`,
        icon: 'question',
        showCloseButton: true,
        showCancelButton: true,
        confirmButtonColor: "#7442DB",
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                type: "POST",
                url: url,
                data: {
                    "id": id,
                    "csrfmiddlewaretoken": getCSRFToken(),
                },
                success: function (data) {
                    if (element_table_id == undefined){
                        location.reload();
                    }
                    else{
                        $(element_table_id).DataTable().ajax.reload(null, false);
                        if (data["message"]) {
                            $.toast({
                                text: data.message,
                                position: 'bottom-right',
                                stack: false,
                                icon: data.level ? data.level : 'success',
                            })
                        }
                    }
                }
            });
        }
    })
})