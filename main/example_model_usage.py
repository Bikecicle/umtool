from model import ServerListPoller

def main():
    host_list = ["eb2-2214-sd01ipmi.csc.ncsu.edu"]  # Fill this in appropriately

    text_file_prefix = "report_file.txt"  # For now, this is the actual file path rather than
    # The prefix. This will need to change when we have lots of servers

    save_method = "dpt"     # Save to the database (not yet implemented)
                            # Print to standard output
                            # Save to a text file

    server_list_poller = ServerListPoller(host_list,
                                          text_file_prefix=text_file_prefix,
                                          save_method=save_method)

    # Poll all servers once (and save the data appropriately)
    server_list_poller.poll_servers()

if __name__ == '__main__':
    main()
