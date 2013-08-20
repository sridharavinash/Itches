$IDLETIMESECONDS = 60               #number of seconds to consider me idle
$OUTFILE = "c:\Temp\MineMe.csv"     # csv formatted data.

Add-Type @"
  using System;
  using System.Runtime.InteropServices;
  public class Tricks {
    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();
}
"@

Add-Type @'
using System;
using System.Diagnostics;
using System.Runtime.InteropServices;

namespace PInvoke.Win32 {

    public static class UserInput {

        [DllImport("user32.dll", SetLastError=false)]
        private static extern bool GetLastInputInfo(ref LASTINPUTINFO plii);

        [StructLayout(LayoutKind.Sequential)]
        private struct LASTINPUTINFO {
            public uint cbSize;
            public int dwTime;
        }

        public static DateTime LastInput {
            get {
                DateTime bootTime = DateTime.UtcNow.AddMilliseconds(-Environment.TickCount);
                DateTime lastInput = bootTime.AddMilliseconds(LastInputTicks);
                return lastInput;
            }
        }

        public static TimeSpan IdleTime {
            get {
                return DateTime.UtcNow.Subtract(LastInput);
            }
        }

        public static int LastInputTicks {
            get {
                LASTINPUTINFO lii = new LASTINPUTINFO();
                lii.cbSize = (uint)Marshal.SizeOf(typeof(LASTINPUTINFO));
                GetLastInputInfo(ref lii);
                return lii.dwTime;
            }
        }
    }
}
'@
$hash = @{}
while(1){
    $idle =  [PInvoke.Win32.UserInput]::IdleTime
    if($idle.TotalSeconds -lt $IDLETIMESECONDS){
        $a = [tricks]::GetForegroundWindow()
        #Get-Process | ? { $_.mainwindowhandle -eq $a } | Format-List MainWindowTitle | Out-File -Append $OUTFILE
        $title = Get-Process | ? { $_.mainwindowhandle -eq $a } | Select-Object MainWindowTitle,id 
        $key = $title.MainWindowTitle
        if($key -ne $null){
            if($hash.ContainsKey($key)){
               $item = $hash.Get_Item($key);
               $hash.Set_Item($key,$item+1);
            }
             else{
                $hash.Add($key,1);
            }
            if($hash.Count -ge 1){
               $hash.GetEnumerator() | Sort-Object Name |ForEach-Object {"{0},{1}" -f $_.Name,($_.Value -join ",")} |Out-File $OUTFILE
                }

        }
        
        Sleep 1
    }
}
