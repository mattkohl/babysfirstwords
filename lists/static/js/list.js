window.babysFirstWords = {};
window.babysFirstWords.initialize = function () {
  $('input[name="text"]').on('keypress', function () {
    $('.has-error').hide();
  });
};