var tic_tac_toe = function() {

    var $squares;
    var $turn;
    var turn = true; // true if users turn
    var board = []; // 1 - user; 0 - computer;

    function init() {
        console.log('Started tic tac toe');
        board = new_board();
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

    function new_board() {
        var matrix = [];
        for(var i = 0; i < 3; i++) {
            var row = [];
            for(var j = 0; j < 3; j++) {
                row.push(null);
            }
            matrix.push(row);
        }
        return matrix;
    }

    function print_board(b) {
        var str = "";
        for(var i = 0; i < 3; i++) {
            str += printable_char(b[i][0]) + " " + printable_char(b[i][1]) + " " + printable_char(b[i][2]) + "\n";
        }
        console.log(str);
    }

    function printable_char(c) {
        return c == null ? '-' : c;
    }

    /**
     * Receives the current board and the next char to play
     * */
    function get_successors(board, char) {
    }

    function did_click_square() {
        if(!turn) { return; }
        var row = $(this).data('row');
        var column = $(this).data('column');
        var $square = $(this);
        board[row][column] = 1;
        print_board(board);
        user_check($square);
        switch_turn_span();
        switch_turn();
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
    function switch_turn_span() {
        if(turn) {
            $turn.text("Computer's turn");
        } else {
            $turn.text("Your turn");
        }
    }

    function switch_turn() {
        turn = !turn;
    }

    return {
        init: init
    }

}();

$(function() {
    tic_tac_toe.init();
});
