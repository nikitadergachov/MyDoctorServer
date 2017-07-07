

var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-patient").modal("show");
      },
      success: function (data) {
        $("#modal-patient .modal-content").html(data.html_form);


      }
    });

  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#patient-table tbody").html(data.html_patients_list);
          $("#modal-patient").modal("hide");
        }
        else {
          $("#modal-patient .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };
var loadData = function () {
  var data = $('#id_DOB').val();
  var DOB = new Date(data);
    alert($('#id_DOB'));

  $("#id_DOB").val(getFormattedDate(DOB));

};


  function getFormattedDate (date) {
                return date.getFullYear()
                    + "-"
                    + ("0" + (date.getMonth() + 1)).slice(-2)
                    + "-"
                    + ("0" + date.getDate()).slice(-2);
}



  /* Binding */

  // Create patient
  $("#create").click(loadForm);
  $("#modal-patient").on("submit", ".js-patient-create-form", saveForm);

  // Update patient
  $("#patient-table").on("click", "#patient-update", loadForm);
  $("#modal-patient").on("submit", ".patient-update-form", saveForm);

  // Delete patient
  $("#patient-table").on("click", "#patient-delete", loadForm);
  $("#modal-patient").on("submit", ".patient-delete-form", saveForm);





  $("#create_analys").click(function() {
              console.log("Модал");
            //открыть модальное окно с id="myModal"
            $("#modal-analys").modal('show');
          });

    $("#create_medicines").click(function() {
        console.log("Модал");
        //открыть модальное окно с id="myModal"

        $("#modal-medicines").modal('show');

        var availableTags = [
            "Анальгин",
            "Цистон",
            "Парацетомол",
            "Магнирот",
            "Фарингасепт"
        ];

         var availableTagsType = [
            "Таблетка",
            "Капсула",
            "Свеча",
            "Иньекция",
            "Сироп",
            "Капли"

        ];

           var availableTagsReception = [
            "Перерорально",
            "Внутривенно",
            "Внутримышечно",
               "Подкожно",
               "Ректальный"


        ];

        $("#id-body").ready(function () {

              $("input[name=type]").autocomplete({source: [availableTagsType]});
              $("input[name=method_reception]").autocomplete({source: [availableTagsReception]});

        });




    });


     $("#create_procedure").click(function() {
              console.log("Модал");
            //открыть модальное окно с id="myModal"
            $("#modal-procedure").modal('show');
          });

       $("#create_visit").click(function() {
              console.log("Модал");
            //открыть модальное окно с id="myModal"
            $("#modal-visit").modal('show');
          });


                    $('table').dataTable( {
                        "language": {
                            "url": "http://cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Russian.json"

                        }
                    } );








