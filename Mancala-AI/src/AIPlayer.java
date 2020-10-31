import java.util.List;
import java.util.Map;

public class AIPlayer extends Player {
    public static final int INFINITY = 99999;

    int whichHeuristic;
    public AIPlayer(int playerNo, Board board) {
        super(playerNo, board);
    }

    void setWhichHeuristic(int heuristicNum){
        whichHeuristic = heuristicNum;
    }

    @Override
    void makeMove() {
        int height = Game.DIFFICULTY_LEVEL;
        int bestVal = -INFINITY;
        int whichCell = -1;
        int alpha = -INFINITY;
        int beta = INFINITY;

        for(int i=1;i<=6;i++){
            Board childNode = new Board(board);
            boolean isValidMove = childNode.moveOnCell(i,myPlayerID);

            if(isValidMove){
                int retVal = 0;

                if(childNode.isAgainTurn()){
                    retVal = miniMax(childNode,height-1,true,alpha,beta,myPlayerID);
                }else{
                    retVal = miniMax(childNode,height-1,false,alpha,beta,(myPlayerID+1)%2);
                }
                alpha = Math.max(alpha,bestVal);
                if(retVal >  bestVal){
                    bestVal = retVal;
                    whichCell = i;
                }
                if(beta <= alpha){
                    break;
                }


            }

        }

        board.moveOnCell(whichCell, myPlayerID);

        if(!Game.isSimulation)
            board.printBoard();
        if(board.isAgainTurn() && !board.isGameFinished()){
            makeMove();
        }
    }

    private int miniMax(Board board,int height,boolean isMaximizingPlayer,int alpha,int beta,int playerNo){

        if(height ==0 || board.isGameFinished()){
            //System.out.println("heuristic "+board.getHeuristicValue(playerNo)+" Player "+playerNo);
            //board.printBoard();
            int ans;
            ans =  board.getHeuristicValue(myPlayerID,whichHeuristic);
            //System.out.println(ans);
            return ans;
        }

        int bestVal = 0;
        List<Board> allPssbleMoves = board.getAllMovesFor(playerNo);
        if(isMaximizingPlayer){
            bestVal = -INFINITY;
            for(Board childNode:allPssbleMoves){
                int retVal = 0;

                if(childNode.isAgainTurn()){
                    retVal = miniMax(childNode,height-1,isMaximizingPlayer,alpha,beta,playerNo);
                }else{
                    retVal = miniMax(childNode,height-1,!isMaximizingPlayer,alpha,beta,(playerNo+1)%2);
                }
                bestVal = Math.max(retVal, bestVal);
                alpha = Math.max(alpha,bestVal);
                if(beta <= alpha){
                    break;
                }
            }
        }else{
            bestVal = INFINITY;
            for(Board childNode : allPssbleMoves){
                int retVal = 0;
                if(childNode.isAgainTurn()){
                    retVal = miniMax(childNode,height-1,isMaximizingPlayer,alpha,beta,playerNo);
                }else{
                    retVal = miniMax(childNode,height-1,!isMaximizingPlayer,alpha,beta,(playerNo+1)%2);
                }
                bestVal = Math.min(bestVal,retVal);
                beta = Math.min(bestVal,beta);
                if(beta <= alpha){
                    break;
                }
            }
        }
        return bestVal;
    }
}
