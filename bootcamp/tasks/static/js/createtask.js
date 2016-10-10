$(function () {
  $(".create").click(function () {
    $("input[name='status']").val("A");
    $("form").submit();
  });

  $(".run").click(function () {
    $("input[name='status']").val("D");
    $("form").submit();
  });

});

