# internet-speed-monitor

A simple internet speed monitor that
- Sets up a crontab to run an internet speedtest every 5 minutes
- Sets up a a service that provides a web UI

## How to use
1. Clone this repository: `git clone https://github.com/oskarkraak/internet-speed-monitor.git`
1. Run `internet-speed-monitor/setup.sh`
1. Navigate to your device on port 5000 in your web browser (`http://[YOUR_IP]:5000`)

In case you want to see the logs, run `sudo journalctl -u internet-speed-monitor.service -f`.
Should you want to restart the service, e.g. after making changes to the code, run `bash restart.sh`.
