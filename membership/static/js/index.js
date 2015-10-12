$(function () {
  $('.button-index').click(function (e) {
    var $this = $(this);
    var href;
    switch (e.which) {
      case 1:
        e.preventDefault();
        href = $this.find('a').attr('href');
        document.location = href;
        break;
      case 2:
        e.preventDefault();
        href = $this.find('a').attr('href');
        window.open(href, '_blank');
        break;
      default:
        break;
    }
  });
});