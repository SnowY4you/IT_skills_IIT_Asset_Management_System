from ldapserver import Server as MockLDAPServer
import time  # For keeping the server running

def run_mock_ldap_server(port=3890):
    mock_server = MockLDAPServer(port=port)
    mock_server.start()
    print(f"Mock LDAP server started on port {port}")

    try:
        while True:  # Keep the server running
            time.sleep(1)  # Or some other suitable interval
    except KeyboardInterrupt:
        print("Stopping mock LDAP server...")
    finally:
        mock_server.stop()
        print("Mock LDAP server stopped.")

if __name__ == "__main__":
    run_mock_ldap_server()