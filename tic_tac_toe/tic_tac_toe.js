var tic_tac_toe = function() {

    var $squares;
    var $turn;
    var turn = true;

    function init() {
        console.log('Started tic tac toe');
        cache_dom();
        bind_events();
    }

    function cache_dom() {
        $squares = $('.square');
        $turn = $('.turn');
    }

    function bind_events() {
        $squares.on('click', did_click_square);
    }

    function did_click_square() {
        var row = $(this).data('row');
        var column = $(this).data('column');
        var $square = $(this);
        user_check($square);
        toggle_turn();
    }

    function user_check(elem) {
        mark_with(elem, 'x');
    }

    function computer_check(elem) {
        mark_with(elem, 'o');
    }

    function mark_with(elem, symbol) {
        $(elem).css('background-image', "url('" + symbol + ".png')");
    }

    // true if users
    function toggle_turn() {
        if(turn) {
            $turn.text("Computer's turn");
        } else {
            $turn.text("Your turn");
        }
        turn = !turn;
    }

    return {
        init: init
    }

}();

$(function() {
    tic_tac_toe.init();
});
