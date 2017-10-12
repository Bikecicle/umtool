import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

/**
 * 
 */

/**
 * @author Matt
 *
 */
public class Parser {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Scanner scan;
		try {
			scan = new Scanner(new File(args[0]));
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			scan = new Scanner(System.in);
			e.printStackTrace();
		}
		//1 minute load average
		String load1Min = "";
		//5 minute load average
		String load5Min = "";
		//15 minute load average
		String load15Min = "";
		//How much CPU the user is taking up, percentage
		String cpuUser = "";
		//How much CPU the system is taking up, percentage
		String cpuSys = "";
		//How much CPU has the "nice" priority tag, percentage
		String cpuNice = "";
		//How much CPU is idle, percentage
		String cpuIdle = "";
		//How much CPU is waiting, percentage
		String cpuWait = "";
		//How much CPU is serving a hardware interrupt, percentage
		String cpuHardInterrupt = "";
		//How much CPU is serving a software interrupt, percentage
		String cpuSoftInterrupt = "";
		//How much CPU is stolen by VMs, percentage
		String cpuStolen = "";
		//How much RAM is unused, KiB
		String freeRam = "";
		//How much RAM is used, KiB
		String usedRam = "";
		//How much swap space is free, KiB
		String freeSwap = "";
		//How much swap space is used, KiB
		String usedSwap = "";
		//Iterate until the end of the file for data
		while( scan.hasNext() ){
			//Pull the first token of the line
			String item = scan.next();
			//Search for the token values that we want to act on and ignore the rest
			//scan.next(); mid-line to skip unwanted tokens
			//This approach taken to avoid as many string writes as possible, Java is very slow with string manipulation
			if( item.equals("top")){
				while( !scan.next().equals("average:")){
				}
				load1Min = scan.next();
				load5Min = scan.next();
				load15Min = scan.next();
			} else if( item.equals("%Cpu(s):")){
				cpuUser = scan.next();
				scan.next();
				cpuSys = scan.next();
				scan.next();
				cpuNice = scan.next();
				scan.next();
				cpuIdle = scan.next();
				scan.next();
				cpuWait = scan.next();
				scan.next();
				cpuHardInterrupt = scan.next();
				scan.next();
				cpuSoftInterrupt = scan.next();
				scan.next();
				cpuStolen = scan.next();
			} else if ( item.equals("KiB")){
				if( scan.next().equals("Mem")){
					scan.next();
					scan.next();
					scan.next();
					freeRam = scan.next();
					scan.next();
					usedRam = scan.next();
				} else {
					scan.next();
					scan.next();
					freeSwap = scan.next();
					scan.next();
					usedSwap = scan.next();
				}
			}
			//Hop to the next line and begin reading again
			scan.nextLine();
			
		}
	}

}
