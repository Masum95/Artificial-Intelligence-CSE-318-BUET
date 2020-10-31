import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

public class Board{

    public static final int STONE_IN_HOLE = 4;
    public int w1 = 5,w2 = 1,w3 = 2,w4  = 1;

    int[][] holes= new int[2][7]; // 2 row and 6 holes in each
    private boolean isAgainTurn = false;
    int heuristicValue, stonesCapturedInLastMove =0; // eta bujhi nai ;
    int lastMoveOnWhichCell;

    Board(){
        for(int i=0;i<2;i++) {
            Arrays.fill(holes[i], Board.STONE_IN_HOLE);
        }
        holes[0][6] = holes[1][6] = 0;

    }

    Board(Board board){
        isAgainTurn = board.isAgainTurn;

        for(int i=0;i<2;i++){
            for(int j=0;j<7;j++){
                holes[i][j] = board.holes[i][j];
            }
        }
    }

    public int getHeuristicValue(int playerNo,int whichHeuristic){
        if(whichHeuristic == 1) return runHeuristic1(playerNo);
        else if(whichHeuristic == 2) return runHeuristic2(playerNo);
        else if(whichHeuristic == 3) return runHeuristic3(playerNo);
        else return runHeuristic4(playerNo);
    }

    private int runHeuristic1(int playerNo){
        return getStorageFor(playerNo) - getStorageFor((playerNo+1)%2);
    }

    private int runHeuristic2(int playerNo){
        return w1*(getStorageFor(playerNo) - getStorageFor((playerNo+1)%2)) +
                w2* (getStonesOnSide(playerNo) - getStonesOnSide((playerNo+1)%2));
    }

    private int runHeuristic3(int playerNo){
        return w1*(getStorageFor(playerNo) - getStorageFor((playerNo+1)%2)) +
                w2* (getStonesOnSide(playerNo) - getStonesOnSide((playerNo+1)%2)) +
                w3* (isAgainTurn == true? 1 :0);
    }

    private int runHeuristic4(int playerNo){

        return w1*(getStorageFor(playerNo) - getStorageFor((playerNo+1)%2)) +
                w2* (getStonesOnSide(playerNo) - getStonesOnSide((playerNo+1)%2)) +
                w3* (isAgainTurn == true? 1 :0) +
                w4*  ( stonesCapturedInLastMove );
    }

    private int getStorageFor(int playerNo){
        return holes[playerNo][6];
    }


    private int getStonesOnSide(int playerNo){
        int sum = 0;
        for(int i=0;i<6;i++) {
            sum+= holes[playerNo][i];
        }
        return sum;
    }

    boolean isZeroStoneOnMySide(int playerNo){
        int sum = 0;
        for(int i=0;i<6;i++){
            sum+= holes[playerNo][i];
        }
        return sum == 0;
    }

    void captureAllRemainingStones(int playerNo){
        for(int i=0;i<6;i++){
            holes[playerNo][6] += holes[playerNo][i];
            holes[playerNo][i] = 0;
        }
    }

    boolean isGameFinished(){
        return isZeroStoneOnMySide(Player.FIRST_PLAYER) || isZeroStoneOnMySide(Player.SECOND_PLAYER);
    }

    int getWinner(){
        if(!isGameFinished()) return -1;
        if(getStorageFor(Player.FIRST_PLAYER) == getStorageFor(Player.SECOND_PLAYER)) return -1;
        if(getStorageFor(Player.FIRST_PLAYER) > getStorageFor(Player.SECOND_PLAYER)) return Player.FIRST_PLAYER;
        else return Player.SECOND_PLAYER;
    }

    void printBoard(){
        //First Line
        System.out.print(" |\t  |");
        System.out.print("\t");
        for(int j=5;j>=0;j--){
            System.out.printf("|%2d|\t",holes[0][j]);
        }
        System.out.print(" |\t  |");

        //Second Line
        System.out.println();
        System.out.printf(" | %2d |",getStorageFor(Player.FIRST_PLAYER));
        System.out.printf(" ------------------------------------------------");
        System.out.printf(" | %2d |",getStorageFor(Player.SECOND_PLAYER));

        //Third Line
        System.out.println();
        System.out.print(" |\t  |");
        System.out.print("\t");
        for(int j=0;j<6;j++){
            System.out.printf("|%2d|\t",holes[1][j]);
        }
        System.out.print(" |\t  |");
        System.out.println();
        System.out.println();
    }

    public List<Board> getAllMovesFor(int playerNo) {
        List<Board> allPssbleMoves = new ArrayList<>();

        for(int i=1;i<=6;i++){
            Board board = new Board(this);
            boolean isValidMove = board.moveOnCell(i,playerNo);
            if(isValidMove){
                allPssbleMoves.add(board);
            }
        }
        return allPssbleMoves;
    }

    private boolean isMyStorage(int row,int col,int playerNo){
        if(playerNo==Player.FIRST_PLAYER) return (row == 0 && col == 6);
        else return (row == 1 && col == 6);
    }

    boolean isAgainTurn(){
        return isAgainTurn;
    }

    //cell valued from 1 to 6
    // returns whether a valid move
    public boolean moveOnCell(int cell, int playerNo) {
        if(cell<1 || cell>6) return false;
        isAgainTurn = false;
        stonesCapturedInLastMove = 0;
        int row =0,col = cell - 1;
        lastMoveOnWhichCell = cell;
        if(playerNo == Player.FIRST_PLAYER){
            row = 0;
        }else if(playerNo == Player.SECOND_PLAYER) {
            row = 1;
        }
        int stoneOnCell = holes[row][col];
        if(stoneOnCell == 0){
            return false; // invalid move;
        }
        holes[row][col] = 0;
        while(stoneOnCell>0){
            col++;
            if(col == 7){
                row = (row+1)%2;
                col = 0;
            }

            if(row == (playerNo+1)%2 && col == 6){
                continue;                           //if opponent's storage, skip it
            }
            holes[row][col]++;
            stoneOnCell--;
        }

        if(isMyStorage(row,col,playerNo)){
            isAgainTurn = true;
        }

        if(row == playerNo){ // if last move was on the Player's row
            if(holes[row][col] == 1 && col<6){ //  if last move was on an empty cell say X
                holes[row][6]+= holes[row][col] + holes[(row+1)%2][5-col]; // then add all the stones of X &
                // the exact opposite cell of X to my storage
                stonesCapturedInLastMove = holes[row][col] + holes[(row+1)%2][5-col];
                holes[row][col] = holes[(row+1)%2][5-col] =  0;
            }
        }

        if(isZeroStoneOnMySide(playerNo)){
            captureAllRemainingStones((playerNo+1)%2);
        }
        return true;
    }


}
