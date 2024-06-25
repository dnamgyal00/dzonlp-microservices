// Import the JavaWylie package.
import org.rigpa.wylie.Wylie;
import java.util.Scanner;

// Import file handling packages.
import java.io.File;
import java.io.IOException;


public class CustomToWylie {
    public static void main(String[] args) {
        // Get the argument:
        String argument = args[0];
        // System.out.println("argument = " + argument);

        // Converts the Dzongkha argument to Wylie:
        Wylie wl = new Wylie();
        //String result = wl.toWylie(argument, null, true);
        String result = wl.toWylie(argument);
        // System.out.println("Wylie: " + result);

        // Write the result to a file:
        try {
            File file = new File("result.txt");
            java.io.PrintWriter output = new java.io.PrintWriter(file);
            System.out.println(result);
            output.println(result);
            System.out.println("1");
            output.close();
        } catch (IOException ex) {
            System.out.println("0");
            System.out.println("Error writing to file.");
            ex.printStackTrace();
        }

    }
}
