import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class Demo {
    public static void main(String[] args) throws FileNotFoundException {

        System.out.println("Enter 1 for Computer Vs Computer");
        System.out.println("Enter 2 for Computer Vs Human");
        System.out.println("Enter 3 for Human Vs Human");

        Scanner sc = new Scanner(System.in);
        int modeChoice = sc.nextInt();
        Board board = new Board();
        Player player1 = null, player2 = null;
        int player1Win = 0, player2Win=0;
        //if computer vs computer
        if(modeChoice == 1){
            sc = new Scanner(new File("input.txt"));
            while(sc.hasNext()) {

                player1 = new AIPlayer(Player.FIRST_PLAYER, board);
                player2 = new AIPlayer(Player.SECOND_PLAYER, board);

                int whichHeuristic = sc.nextInt();              //input : first player heuristic
                ((AIPlayer) player1).setWhichHeuristic(whichHeuristic);

                whichHeuristic = sc.nextInt();                  //input : second player heuristic
                ((AIPlayer) player2).setWhichHeuristic(whichHeuristic);

                Game game = new Game(player1, player2, board);
                System.out.println("Enter difficulty level");
                Game.DIFFICULTY_LEVEL = sc.nextInt();           //input : tree depth
                Game.isSimulation = true;
                int winner = game.startGame();
                System.out.println(((AIPlayer) player1).whichHeuristic + " - "+((AIPlayer) player2).whichHeuristic + " "+ Game.DIFFICULTY_LEVEL);
                if (winner == Player.FIRST_PLAYER) {
                    System.out.println("player 1 wins");
                    player1Win++;
                } else if (winner == Player.SECOND_PLAYER){
                    System.out.println("player 2 wins");
                    player2Win++;
                }else{
                   // System.out.println("drawn");
                }

            }
            double total = player1Win+player2Win;
            double per1 = player1Win/total*100;
            double per2 = player2Win/total*100;
            System.out.println("Player 1 win % "+per1);
            System.out.println("Player 2 win % "+per2);

        }

        else {
            // computer vs human
            if (modeChoice == 2) {
                player1 = new AIPlayer(Player.FIRST_PLAYER, board);
                player2 = new HumanPlayer(Player.SECOND_PLAYER, board);

            }else{ // human vs human
                player1 = new HumanPlayer(Player.FIRST_PLAYER, board);
                player2 = new HumanPlayer(Player.SECOND_PLAYER, board);
            }

            if (modeChoice == 2) {
                System.out.println("Enter Heuristic to run for Player 1 (1-4)");
                int whichHeuristic = sc.nextInt();
                ((AIPlayer) player1).setWhichHeuristic(whichHeuristic);
                System.out.println("Enter Difficulty Level  "); // this is actually input of iterative deepening search's depth
                Game.DIFFICULTY_LEVEL = sc.nextInt();

            }

            Game game = new Game(player1, player2, board);
            int winner = game.startGame();
            System.out.println();
            if (winner == Player.FIRST_PLAYER) {
                System.out.println("---Player 1 has won---");
                player1Win++;
            } else if (winner == Player.SECOND_PLAYER){
                System.out.println("---Player 2 has won---");
                player2Win++;
            }else{
                System.out.println("---Match Drawn---");
            }

        }


    }
}
