function TreeNode(state) {
    this.state = state;
    this.score = null;
    this.children = [];
    this.i = -1;
    this.j = -1;
}

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

    function get_successors(board, t) {
        var pl = player(t);
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
        board[row][column] = player(turn);
        user_check($square);
        switch_turn_span();
        switch_turn();
        check_game_over();
        computer_turn();
    }

    // TODO Minimax
    function computer_turn() {
        if(game_over || turn) { return; }
        var node = minimax(board);
        board[node.i][node.j] = player(turn);
        var index = node.i*3 + node.j;
        computer_check($($squares[index]));
        switch_turn_span();
        check_game_over();
        switch_turn();
    }

    function score_state(state) {
        for(var i = 0; i < 3; i++) {
            // Horizontal
            if(state[i][0] != null && state[i][0] == state[i][1] && state[i][1] == state[i][2]) {
                return state[i][0] == 1 ? 1 : -1;
            }
            // Vertical
            if(state[0][i] != null && state[0][i] == state[1][i] && state[1][i] == state[2][i]) {
                return state[0][i] == 1 ? 1 : -1;
            }
        }
        // Diagonal Top Left - Bottom Right
        if(state[0][0] != null && state[0][0] == state[1][1] && state[1][1] == state[2][2]) {
            return state[0][0] == 1 ? 1 : -1;
        }
        // Diagonal Top Right - Bottom Left
        if(state[0][2] != null && state[0][2] == state[1][1] && state[1][1] == state[2][0]) {
            return state[0][2] == 1 ? 1 : -1;
        }
        return 0;
    }

    function minimax(state, t) {

        var depth = 2;
        var root = new TreeNode(clone_board(state));

        var v = 2; // Min
        x_value(root, t, depth, v, Math.min, Math.max);

        for(var i = 0; i < root.children.length; i++) {
            if(root.children[i].score == root.score) {
                return root.children[i];
            }
        }

        // TODO Find random
        return null;
    }

    function x_value(node, t, depth, v, f, o) {

        var score = score_state(node.state);
        if(depth == 0 || score != 0) {
            node.score = score;
            return score;
        }

        // TODO Needs improvement
        var successors = get_successors(node.state, t);
        for(var i = 0; i < successors.length; i++) {
            var tn = new TreeNode(successors[i][0]);
            tn.i = successors[i][1];
            tn.j = successors[i][2];
            node.children.push(tn);
        }

        node.score = v;
        for(var i = 0; i < successors.length; i++) {
            var curr = node.children[i];
            node.score = f(node.score, x_value(curr, !t, depth-1, -v, o, f));
        }

        return node.score

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

    function player(t) {
        return t ? 1 : 0;
    }

    function is_game_over(board) {
        return score_state(board) != 0;
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
