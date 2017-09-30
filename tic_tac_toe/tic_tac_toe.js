var tic_tac_toe = function() {

    var $squares;

    function init() {
        console.log('Started tic tac toe');
        cache_dom();
        bind_events();
    }

    function cache_dom() {
        $squares = $('.square');
    }

    function bind_events() {
        $squares.on('click', did_click_square);
    }

    function did_click_square() {
        var row = $(this).data('row');
        var column = $(this).data('column');
        console.log(row + "  " + column);
    }

    return {
        init: init
    }

}();

$(function() {
    tic_tac_toe.init();
});
