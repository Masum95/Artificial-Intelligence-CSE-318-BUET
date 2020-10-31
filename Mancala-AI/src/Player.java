
public abstract class Player {
    public static final int FIRST_PLAYER = 0;
    public static final int SECOND_PLAYER = 1;

    int myPlayerID;
    Board board;

    public Player(int playerNo, Board board) {
        this.board = null;
        this.myPlayerID = playerNo;
        this.board = board;
    }

    abstract void makeMove();
}

