import java.util.List;
import java.util.Scanner;

public class HumanPlayer extends Player {

    HumanPlayer(int playerNo, Board board){
        super(playerNo,board);
    }

    void makeMove(){
        System.out.println("Input the cell number you want to make move (1-6)");

        Scanner sc = new Scanner(System.in);
        int cell;
        while(true){
            cell = sc.nextInt();
            if(cell>6 || cell<1) {
                System.out.println("Invalid move, Please make a valid move");
            }
            else break;
        }

        boolean isValidMove = board.moveOnCell(cell,myPlayerID);
        if(!isValidMove){
            System.out.println("Invalid move. Please make a valid move");
        }
        if(!Game.isSimulation)
            board.printBoard();
        if(!isValidMove || board.isAgainTurn()){
            makeMove();
        }

    }
}
