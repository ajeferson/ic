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

    function clone_board(board) {
        var cl = new_board();
        for(var i = 0; i < board.length; i++) {
            for(var j = 0; j < board[0].length; j++) {
                cl[i][j] = board[i][j];
            }
        }
        return cl;
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

    function get_successors(board) {
        var pl = player();
        var successors = [];
        for(var i = 0; i < board.length; i++) {
            for(var j = 0; j < board[0].length; j++) {
                if(board[i][j] == null) {
                    var s = clone_board(board);
                    s[i][j] = pl;
                    successors.push([s, i, j]);
                }
            }
        }
        return successors;
    }

    function did_click_square() {
        if(!turn) { return; }
        var row = $(this).data('row');
        var column = $(this).data('column');
        var $square = $(this);
        board[row][column] = player();
        user_check($square);
        switch_turn_span();
        switch_turn();
        computer_turn();
    }

    // TODO Minimax
    function computer_turn() {
        var successors = get_successors(board);
        var new_state = successors[0];
        var new_board = new_state[0];
        var row = new_state[1];
        var column = new_state[2];
        board[row][column] = player();
        var index = row*3 + column;
        computer_check($($squares[index]));
        switch_turn_span();
        switch_turn();
        print_board(board);
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

    function player() {
        return turn ? 1 : 0;
    }

    return {
        init: init
    }

}();

$(function() {
    tic_tac_toe.init();
});
