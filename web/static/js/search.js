'use strict';
$(function () {
  var $results = $('#results');
  var $resultsTemplate = $('#results-template');

  // columns to be displayed in order
  var tableColumns = [
    ['Name', 'name'],
    ['Knights email', 'knights_email'],
    ['Paid Dues', 'paid_dues'],
    ['Shirt gender', 'shirt_gender'],
    ['Shirt size', 'shirt_size'],
    ['Form timestamp', 'timestamp']
  ];

  $('input[type=reset]').click(function() {
    $results.find('table').remove();
  });

  $('#search').submit(function (event) {
    event.preventDefault();

    var $this = $(this),
      action = $this.prop('action'),
      data = $this.serialize();

    $.post(action, data).done(function (data) {
      // don't bother if there are no results
      var results = data['results'];
      if (!results || !results['data']) {
        $results.find('table').remove();
        return;
      }

      var $newResults = $resultsTemplate.clone().removeAttr('id').show();

      // generate thead
      var $head = $newResults.find('thead').find('tr');
      tableColumns.forEach(function(col) {
        var pretty = col[0];
        $head.append($('<th></th>').text(pretty));
      });

      // generate tbody
      var $tbody = $newResults.find('tbody');
      results['data'].forEach(function(member) {
        var $row = $('<tr></tr>');

        tableColumns.forEach(function(col) {
          var key = col[1];
          var value = member[key];
          if (key === 'paid_dues') {
            value =  value ? '✓' : '✗';
          }
          var $td = $('<td></td>').text(value);
          $row.append($td);
        });

        $tbody.append($row);
      });

      $results.find('table').remove();
      $results.append($newResults).show();
    });
  });
});