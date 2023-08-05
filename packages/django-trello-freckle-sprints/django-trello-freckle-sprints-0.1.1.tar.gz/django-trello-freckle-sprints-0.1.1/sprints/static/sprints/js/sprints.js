function update_total() {
    var time_total = 0;
    var cost_total = 0;
    $(':checked').each(function() {
        var card_id = $(this).attr('data-card-id');
        var time = $('[data-time-for="'+ card_id +'"]').html();
        var cost = $('[data-cost-for="'+ card_id +'"]').html();
        time_total += parseFloat(time);
        cost_total += parseFloat(cost);
        $('[data-id="total-time"]').html(time_total);
        $('[data-id="total-cost"]').html(cost_total);
    });
}

$(document).ready(function() {
    $('[data-class="check-card"]').click(function() {
        update_total();
    });
});
