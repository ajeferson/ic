function TreeNode(state) {
    this.state = state;
    this.score = null;
    this.children = [];
    this.i = -1;
    this.j = -1;
}

function TicTacToe() {

    this.$squares = null;
    this.$turn = null;
    this.turn = true; // true if users turn
    this.board = []; // 1 - user; 0 - computer;
    this.game_over = false;

    this.init = function() {
        this.cache_dom();
        this.bind_events();
        this.board = this.new_board();
        // this.board[0][0] = 0;
        // this.board[0][1] = 0;
        // this.board[0][2] = 1;
        // this.board[1][1] = 1;
        // this.board[2][0] = 0;
        // this.board[2][1] = 1;
        this.draw_board(this.board);
    };

    this.cache_dom = function() {
        this.$squares = $('.square');
        this.$turn = $('.turn');
    };

    this.bind_events = function() {
        // this.did_click_square.bind(this);
        this.$squares.on('click', this.did_click_square);
    };

    this.new_board = function() {
        var matrix = [];
        for(var i = 0; i < 3; i++) {
            var row = [];
            for(var j = 0; j < 3; j++) {
                row.push(null);
            }
            matrix.push(row);
        }
        return matrix;
    };

    // Draws only when the next move if from the user
    this.draw_board = function(board) {
        for(var i = 0; i < 3; i++) {
            for(var j = 0; j < 3; j++) {
                if(board[i][j] == 1) {
                    this.user_check($(this.$squares[3*i + j]));
                } else if(board[i][j] == 0) {
                    this.computer_check($(this.$squares[3*i + j]));
                }
            }
        }
    };

    this.clone_board = function(board) {
        var cl = this.new_board();
        for(var i = 0; i < board.length; i++) {
            for(var j = 0; j < board[0].length; j++) {
                cl[i][j] = board[i][j];
            }
        }
        return cl;
    };

    this.print_board = function(b) {
        var str = "";
        for(var i = 0; i < 3; i++) {
            str += this.printable_char(b[i][0]) + " " + this.printable_char(b[i][1]) + " " + this.printable_char(b[i][2]) + "\n";
        }
        console.log(str);
    };

    this.printable_char = function(c) {
        return c == null ? '-' : c;
    };

    this.get_successors = function(board, t) {
        var pl = this.player(t);
        var successors = [];
        for(var i = 0; i < board.length; i++) {
            for(var j = 0; j < board[0].length; j++) {
                if(board[i][j] == null) {
                    var s = this.clone_board(board);
                    s[i][j] = pl;
                    successors.push([s, i, j]);
                }
            }
        }
        return successors;
    };

    this.did_click_square = function(e) {
        if(this.game_over || !this.turn) { return; }
        var $target = $(e.target);
        var row = $target.data('row');
        var column = $target.data('column');
        var $square = $target;
        this.board[row][column] = this.player(this.turn);
        this.user_check($square);
        this.switch_turn_span();
        this.switch_turn();
        this.check_game_over();
        this.computer_turn();
    }.bind(this);

    this.computer_turn = function() {
        if(this.game_over || this.turn) { return; }
        var node = this.minimax(this.board);
        this.board[node.i][node.j] = this.player(this.turn);
        var index = node.i*3 + node.j;
        this.computer_check($(this.$squares[index]));
        this.switch_turn_span();
        this.check_game_over();
        this.switch_turn();
    };

    this.score_state = function(state) {
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
    };

    this.minimax = function(state, t) {

        var depth = 2;
        var root = new TreeNode(this.clone_board(state));

        var v = 2; // Min
        this.x_value(root, t, depth, v, Math.min, Math.max);

        for(var i = 0; i < root.children.length; i++) {
            if(root.children[i].score == root.score) {
                return root.children[i];
            }
        }

        // TODO Find random
        return null;

    };

    this.x_value = function(node, t, depth, v, f, o) {

        var score = this.score_state(node.state);
        if(depth == 0 || score != 0) {
            node.score = score;
            return score;
        }

        // TODO Needs improvement
        var successors = this.get_successors(node.state, t);
        for(var i = 0; i < successors.length; i++) {
            var tn = new TreeNode(successors[i][0]);
            tn.i = successors[i][1];
            tn.j = successors[i][2];
            node.children.push(tn);
        }

        node.score = v;
        for(var i = 0; i < successors.length; i++) {
            var curr = node.children[i];
            node.score = f(node.score, this.x_value(curr, !t, depth-1, -v, o, f));
        }

        return node.score

    };

    this.user_check = function(elem) {
        this.mark_with(elem, 'x');
    };

    this.computer_check = function(elem) {
        this.mark_with(elem, 'o');
    };

    this.mark_with = function(elem, symbol) {
        $(elem).css('background-image', "url('" + symbol + ".png')");
    };

    // true if users
    this.switch_turn_span = function() {
        if(this.turn) {
            this.$turn.text("Computer's turn");
        } else {
            this.$turn.text("Your turn");
        }
    };

    this.switch_turn = function() {
        this.turn = !this.turn;
    };

    this.player = function(t) {
        return t ? 1 : 0;
    };

    this.is_game_over = function(board) {
        return this.score_state(board) != 0;
    };

    this.has_room = function(board) {
        for(var i = 0; i < 3; i++) {
            for(var j = 0; j < 3; j++) {
                if(board[i][j] == null) {
                    return true;
                }
            }
        }
        return false;
    };

    this.check_game_over = function() {
        this.game_over = this.is_game_over(this.board);
        if(this.game_over) {
            this.set_game_over_span();
        } else {
            if(!this.has_room(this.board)) { //Tie
                this.game_over = true;
                this.set_tie_span();
            }
        }
    };

    this.set_game_over_span = function() {
        this.$turn.text('Game Over!');
    };

    this.set_tie_span = function() {
        this.$turn.text("It's a Tie!");
    };

}

$(function() {
    var ticTac = new TicTacToe();
    ticTac.init();
});
