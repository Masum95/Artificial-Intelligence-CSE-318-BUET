import java.awt.*;
import java.util.*;
import java.util.List;

class Constants{
    public static int missionaries,cannibals;
    public static int boatCapacity;
    public static Vector<Point> move;
    Constants(int boatCapacity)
    {
        Constants.boatCapacity = boatCapacity;
        move = new Vector<>();
        for(int i=0;i<=boatCapacity;i++){
            for(int j=0;j<=boatCapacity;j++){
                if(i+j>boatCapacity) break;
                if(i+j==0) continue;
                move.add(new Point(i,j));
            }
        }

    }

}

class State {
    int misnrFrom,misnrTo,canblFrom,canblTo;
    boolean onStartSide;
    State parent;
    int n1,n2;

    public State(int misnr, int canbl){
        this.n1=Constants.missionaries;
        this.n2 = Constants.cannibals;

        this.misnrFrom = misnr;
        this.canblFrom = canbl;
        this.onStartSide = true;

        misnrTo=n1-misnr;
        canblTo=n2-canbl;
    }

    public State(int misnr, int canbl, boolean onStartSide) {
        this.n1=Constants.missionaries;
        this.n2 = Constants.cannibals;
        if(!onStartSide){               //if boat isn't on startSide reduce the missionaries/cannibals number
            this.misnrFrom = misnr;
            this.canblFrom = canbl;
            this.onStartSide = onStartSide;

            misnrTo=n1-misnr;
            canblTo=n2-canbl;
        }else{
            this.misnrTo = misnr;
            this.canblTo = canbl;
            this.onStartSide = onStartSide;

            misnrFrom=n1-misnrTo;
            canblFrom=n2-canblTo;
        }


    }

    boolean isValidState(){
        if(misnrTo<0 || misnrFrom<0 || canblFrom<0 || canblTo<0) return  false;
        if(misnrFrom==0) return misnrTo>=canblTo;
        if(misnrTo==0) return misnrFrom>=canblFrom;
        return ((misnrFrom>=canblFrom) && (misnrTo>=canblTo));
    }

    boolean isGoalState(){
        return ((misnrTo==n1 && canblTo==n2) && !onStartSide);
    }

    boolean isStartState(){
        return ((misnrFrom==n1 && canblFrom==n2) && onStartSide);
    }

    List<State> getSuccessors(){

        List<State> succList = new ArrayList<>();
        for(int i=0;i<Constants.move.size();i++){
            State tmp = null;
            if(onStartSide){
                tmp = new State(misnrFrom-Constants.move.get(i).x,canblFrom-Constants.move.get(i).y,!onStartSide);
            }else{
                tmp = new State(misnrTo-Constants.move.get(i).x,canblTo-Constants.move.get(i).y,!onStartSide);
            }
            if(tmp.isValidState()) {
                tmp.parent = this;
                succList.add(tmp);
            }
        }
        return succList;

    }

    void printState(){
        if(onStartSide){
            System.out.println(misnrFrom+"M,"+canblFrom+"C(B) --- "+misnrTo+"M, "+canblTo+"C");
        }
        else{
            System.out.println(misnrFrom+"M,"+canblFrom+"C --- "+misnrTo+"M, "+canblTo+"C (B)");
        }
    }

    State getParent(){
        return parent;
    }

    @Override
    public int hashCode() {
        return misnrFrom*11 + canblFrom * 13 + (onStartSide==true ? 1:0) * 17;
    }

    @Override
    public boolean equals(Object obj) {
        if(this == obj ) return true;
        if(obj == null) return false;
        State s = (State) obj;
        return (canblFrom==s.canblFrom && misnrFrom == s.misnrFrom &&  onStartSide == s.onStartSide);
    }
}
class TimeoutException extends Exception{
    @Override
    public String toString() {
        return "TimeOut Exception ";
    }
}

class NodeOutException extends Exception{
    @Override
    public String toString() {
        return "Number of Expanded node limit has exceeded ";
    }
}

class StateSpace{
    int n;
    Map<State,Integer> hasVisited = new HashMap<>();
    int nodeExpandedBFS,nodeExpandedDFS;
    int nodeExploredBFS,nodeExploredDFS;
    long dfsTime,bfsTime;
    long timeOut,nodeOut;

    public StateSpace(int missionaries,int cannibals) {
        Constants.missionaries = missionaries;
        Constants.cannibals = cannibals;
    }

    void printSolution(State goalState){
        System.out.println("++++");
        Stack<State> stack = new Stack<>();
        State tmp = goalState;
        while(!tmp.isStartState()){
            stack.push(tmp);
            tmp = tmp.getParent();
        }

        stack.push(tmp);

        while(!stack.empty()){
            tmp = stack.pop();
            tmp.printState();
        }
    }

    void runBFS(){
        long startTime = System.currentTimeMillis();
        State state = new State(Constants.missionaries,Constants.cannibals);

        Queue<State> queue = new LinkedList<>();
        queue.add(state);
        boolean soln = false;
        State tmp = null;

        try{
            while(!queue.isEmpty()){
                if(System.currentTimeMillis()-startTime > timeOut) throw new TimeoutException();
                tmp = queue.remove();

                if(hasVisited.get(tmp) == null){
                    hasVisited.put(tmp,1);
                    nodeExploredBFS++;
                    if(tmp.isGoalState()) {
                        soln = true;
                        break;
                    }else{
                        nodeExpandedBFS++;
                        if(nodeExpandedBFS>=nodeOut) throw new NodeOutException();
                        queue.addAll(tmp.getSuccessors());
                    }
                }
            }
            if(soln) printSolution(tmp);
            else{
                System.out.println("No solution");
            }
        }catch (TimeoutException ex){
            System.out.println(ex);
        }catch (NodeOutException ex){
            System.out.println(ex);
        }finally {
            hasVisited.clear();
        }

        long stopTime = System.currentTimeMillis();
        bfsTime = stopTime - startTime;

    }

    void runDFS(){
        long startTime = System.currentTimeMillis();
        State state = new State(Constants.missionaries,Constants.cannibals);

        boolean soln = false;
        Stack<State> stack = new Stack<>();
        stack.push(state);
        State tmp = null;
        try{
            while(!stack.isEmpty()){
                if(System.currentTimeMillis()-startTime > timeOut) throw new TimeoutException();
                tmp = stack.pop();

                if(hasVisited.get(tmp) == null){
                    hasVisited.put(tmp,1);
                    nodeExploredDFS++;
                    if(tmp.isGoalState()) {
                        soln = true;
                        break;
                    }else{
                        nodeExpandedDFS++;
                        List<State> list = tmp.getSuccessors();
                        if(nodeExpandedDFS>=nodeOut) throw new NodeOutException();

                        stack.addAll(list);
                    }

                }
            }
            if(soln) printSolution(tmp);
            else{
                System.out.println("No solution");
            }
        }catch (TimeoutException ex){
            System.out.println(ex);
        }catch (NodeOutException ex){
            System.out.println(ex);
        }finally {
            hasVisited.clear();
        }

        long stopTime = System.currentTimeMillis();
        dfsTime = stopTime - startTime;
    }

    void execute(){
        timeOut = 300;
        nodeOut = 10000;


        System.out.println("Running BFS---");
        runBFS();
        System.out.println("--------");
        System.out.println("Running DFS ---");
        runDFS();
        System.out.println("--------");
        System.out.println("Performance Measure:- ");
        System.out.print(new String(new char["Explored Nodes\t".length()]).replace("\0", " "));
        System.out.println("BFS \t\t"+"DFS");
        System.out.println("Explored Nodes\t"+nodeExploredBFS+"\t\t"+nodeExploredDFS);
        System.out.println("Expanded Nodes\t"+nodeExpandedBFS+"\t\t"+nodeExpandedDFS);
        System.out.println("Time Required \t"+bfsTime+"\t\t"+dfsTime);
    }

}

class Demo{
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter boat Capacity");
        int cap = sc.nextInt();
        new Constants(cap);
        int missionaries,cannibals;
        System.out.println("Enter number of Missionaries & Cannibals respectively ");

        missionaries = sc.nextInt();
        cannibals = sc.nextInt();
        StateSpace stateSpace = new StateSpace(missionaries,cannibals);
        stateSpace.execute();

    }
}
