from crypto.audit_log import initialize_database, log_event

initialize_database()

log_event(
    sender="Device_A",
    receiver="Device_B",
    event="MESSAGE_SENT",
    message_id="test123",
    status="SUCCESS"
)

log_event(
    sender="Device_A",
    receiver="Device_B",
    event="SIGNATURE_VERIFICATION",
    message_id="test123",
    status="SUCCESS"
)

log_event(
    sender="Device_A",
    receiver="Device_B",
    event="TAMPERING_DETECTED",
    message_id="test456",
    status="FAILED"
)

print("Audit logging test completed.")