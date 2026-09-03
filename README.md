PLEASE READ THE REPORT AND FOLLOW THE INSTRUCTIONS PROVIDED THERE

A Network Access Control (NAC) system was built specifically for
institutions to resolve the current necessity for secure network access within environments where
internet usage is widespread and BYOD policy is prevalent. Under VirtualBox control of four
virtual machines (Switch-VM, Policy-Server, Client-1, Client-2) the system fulfills its four
functional requirements through open-source tools (FreeRADIUS, hostapd, wpasupplicant,
compliance_check.py, nac_control.sh, iptables, metrics_exporter.py, Prometheus, and Grafana) to
provide 802.1X authentication with OS compliance checks and dynamic access control along with
real-time monitoring. Through its NAC system the network allows authorized devices with
compliant operating systems to connect effectively blocking unauthorized people and outdated
software. The testing confirmed system success rates where access control reached 98% and
authentication succeeded completely for legitimate credentials. The research examines legal,
social and ethical matters including privacy regulations covered by Nepal’s Individual Privacy Act,
2018 and how the system affects users with non-modern devices. A major benefit includes both
affordable implementation and endless scalability and a solid security framework yet the system
presents challenges due to high resource requirements and difficult user operations. Future
development work includes creating virtualization that uses less system resources while ensuring
user-friendly interfaces that work with older devices. The solution provides institutions with a
secure practical system which adapts well to the balance between technical progress and local
operational realities.
