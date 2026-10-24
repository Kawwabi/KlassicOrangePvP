import java.nio.file.*;
import java.util.*;
import java.util.zip.*;

public class CheckZip {
    public static void main(String[] a) throws Exception {
        try (ZipFile z = new ZipFile(a[0])) {
            int n = 0;
            for (Enumeration<? extends ZipEntry> e = z.entries(); e.hasMoreElements();) {
                try (var in = z.getInputStream(e.nextElement())) { in.readAllBytes(); }
                n++;
            }
            ZipEntry t = z.getEntry(a[1]);
            if (t == null) { System.err.println("entry missing"); System.exit(1); }
            byte[] got = z.getInputStream(t).readAllBytes();
            if (!Arrays.equals(got, Files.readAllBytes(Path.of(a[2])))) {
                System.err.println("entry content mismatch"); System.exit(1);
            }
            System.out.println("OK: " + n + " entries readable, star matches");
        }
    }
}
