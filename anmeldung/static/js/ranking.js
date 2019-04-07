$(document).ready(function() {
  var border = $("#personal-border");
  var userMenu = $(".user-menu");
  var userBlock = $(".user-block");

  $(".dropup-icon").hide();

$('#dtOrderExample').DataTable({
"order": [[ 3, "desc" ]]
});
$('.dataTables_length').addClass('bs-select');


$(document).ready(function () {
  $('#dtBasicExample').DataTable();
  $('.dataTables_length').addClass('bs-select');
)

  $(".menu-icon").click(function() {
    if ($(".nav-links").hasClass("menu-slide-down")) {
      $(".nav-links").removeClass("menu-slide-down");
      $(".nav-links").addClass("menu-slide-up");
    } else {
      $(".nav-links").removeClass("menu-slide-up");
      $(".nav-links").addClass("menu-slide-down");
    }
    $(this).toggleClass("active");
    $(".menu-icon").toggleClass("active-icon");
  });

  userBlock.click(function() {
    $(".dropup-icon").toggle();
    $(".dropdown-icon").toggle();
    $(".user-container").toggleClass("active");
    if (userMenu.hasClass("menu-slide-down")) {
      userMenu.removeClass("menu-slide-down");
      userMenu.addClass("menu-slide-up");
    } else {
      userMenu.removeClass("menu-slide-up");
      userMenu.addClass("menu-slide-down");
    }
  });

  userBlock.mouseenter(function() {
    border.removeClass("remove-border");
    border.addClass("animate-border");
  });

  userBlock.mouseleave(function() {
    border.removeClass("animate-border");
    border.addClass("remove-border");
  });

  $(".menu-icon").mouseenter(function() {
    $("#menu-border").removeClass("remove-border");
    $("#menu-border").addClass("animate-border");
  });

  $(".menu-icon").mouseleave(function() {
    $("#menu-border").removeClass("animate-border");
    $("#menu-border").addClass("remove-border");
  });
});
