var tic_tac_toe = function() {

    var $squares;
    var $turn;
    var turn = true; // true if users turn
    var board = []; // 1 - user; 0 - computer;
    var game_over = false;

    function init() {
        cache_dom();
        bind_events();
        board = new_board();
        board[0][0] = 0;
        board[0][1] = 0;
        board[0][2] = 1;
        board[1][1] = 1;
        board[2][0] = 0;
        board[2][1] = 1;
        draw_board(board);
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

    // Draws only when the next move if from the user
    function draw_board(board) {
        for(var i = 0; i < 3; i++) {
            for(var j = 0; j < 3; j++) {
                if(board[i][j] == 1) {
                    user_check($($squares[3*i + j]));
                } else if(board[i][j] == 0) {
                    computer_check($($squares[3*i + j]));
                }
            }
        }
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
        if(game_over || !turn) { return; }
        var row = $(this).data('row');
        var column = $(this).data('column');
        var $square = $(this);
        board[row][column] = player();
        user_check($square);
        switch_turn_span();
        switch_turn();
        check_game_over();
        computer_turn();
    }

    // TODO Minimax
    function computer_turn() {
        if(game_over || turn) { return; }
        var successors = get_successors(board);
        var new_state = successors[0];
        var new_board = new_state[0];
        var row = new_state[1];
        var column = new_state[2];
        board[row][column] = player();
        var index = row*3 + column;
        computer_check($($squares[index]));
        switch_turn_span();
        check_game_over();
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

    function player() {
        return turn ? 1 : 0;
    }

    function is_game_over(board) {
        for(var i = 0; i < 3; i++) {
            // Horizontal
            if(board[i][0] != null && board[i][0] == board[i][1] && board[i][1] == board[i][2]) {
                return true;
            }
            // Vertical
            if(board[0][i] != null && board[0][i] == board[1][i] && board[1][i] == board[2][i]) {
                return true;
            }
        }
        // Diagonal Top Left - Bottom Right
        if(board[0][0] != null && board[0][0] == board[1][1] && board[1][1] == board[2][2]) {
            return true;
        }
        // Diagonal Top Right - Bottom Left
        if(board[0][2] != null && board[0][2] == board[1][1] && board[1][1] == board[2][0]) {
            return true;
        }
        return false;
    }

    function has_room(board) {
        for(var i = 0; i < 3; i++) {
            for(var j = 0; j < 3; j++) {
                if(board[i][j] == null) {
                    return true;
                }
            }
        }
        return false;
    }

    function check_game_over() {
        game_over = is_game_over(board);
        if(game_over) {
            set_game_over_span();
        } else {
            if(!has_room(board)) { //Tie
                game_over = true;
                set_tie_span();
            }
        }
    }

    function set_game_over_span() {
        $turn.text('Game Over!');
    }

    function set_tie_span() {
        $turn.text("It's a Tie!");
    }

    return {
        init: init
    }

}();

$(function() {
    tic_tac_toe.init();
});
