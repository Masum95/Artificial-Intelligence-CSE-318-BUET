import java.util.Random;
import java.util.concurrent.TimeUnit;

public class Game {
    public static boolean isSimulation = false;
    public static int DIFFICULTY_LEVEL;

    Player player1,player2;
    Board board;
    int mode;

    public Game(Player player1, Player player2, Board board) {
        this.player1 = player1;
        this.player2 = player2;
        this.board = board;
    }


    int startGame(){
        boolean is1stPlayerTurn = true;
        while(true){
            if(is1stPlayerTurn){
                if(!isSimulation) System.out.println("Now Player1 move");
                player1.makeMove();
                is1stPlayerTurn = false;

            }else{
                if(!isSimulation) System.out.println("Now Player 2 move");
                player2.makeMove();
                is1stPlayerTurn = true;

            }
            if(board.isGameFinished()){
                return board.getWinner();
            }

        }

    }
}
