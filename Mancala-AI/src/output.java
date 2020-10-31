import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

public class output {
    public static void main(String[] args) throws IOException {
        PrintWriter writer = new PrintWriter("input.txt", "UTF-8");

        for(int h1=1;h1<=4;h1++){
            for(int h2=1;h2<=4;h2++){
                for(int dif=8;dif<=12;dif++){
                   // System.out.println(1+" "+h1+" "+h2+" "+dif+" "+1);
                    writer.println(h1+" "+h2+" "+dif);
                }
            }
        }
        writer.close();
    }
}
