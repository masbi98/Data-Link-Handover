import time
from pymavlink import mavutil

COM_PORT = 'COM6' 
BAUDRATE = 460800

def main():
    print("Starting Low-Latency Real-Time SITL Injector...")
    try:
        receiver = mavutil.mavlink_connection(COM_PORT, baud=BAUDRATE)
        print(f"[OK] Connected to Receiver on {COM_PORT}.")
    except Exception as e:
        print(f"[ERROR] {e}")
        return

    print("[WAIT] Connecting to Mission Planner Bridge (TCP 14556)...")
    sitl = mavutil.mavlink_connection('tcp:127.0.0.1:14556', source_system=255)
    print("[OK] Connected to Bridge! Instant pass-through active.")

    last_heartbeat = 0
    
    while True:
        try:
            current_time = time.time()
            
            # Send heartbeat to keep receiver active (1Hz)
            if current_time - last_heartbeat > 1.0:
                receiver.mav.heartbeat_send(
                    mavutil.mavlink.MAV_TYPE_QUADROTOR,
                    mavutil.mavlink.MAV_AUTOPILOT_ARDUPILOTMEGA,
                    0, 0, 0
                )
                last_heartbeat = current_time

            # Read packet as soon as hardware receives it (blocking=False)
            rx_msg = receiver.recv_match(type='RC_CHANNELS_OVERRIDE', blocking=False)
            if rx_msg:
                # Forward packet immediately to SITL
                sitl.mav.rc_channels_override_send(
                    1, 0, # Target System 1, Target Component 0
                    rx_msg.chan1_raw, rx_msg.chan2_raw,
                    rx_msg.chan3_raw, rx_msg.chan4_raw,
                    rx_msg.chan5_raw, rx_msg.chan6_raw,
                    rx_msg.chan7_raw, rx_msg.chan8_raw
                )
                print(f"\r[Real-Time] Roll: {rx_msg.chan1_raw} | Pitch: {rx_msg.chan2_raw} | Thr: {rx_msg.chan3_raw} | Yaw: {rx_msg.chan4_raw}    ", end="", flush=True)
                
        except KeyboardInterrupt:
            print("\nStopped.")
            break
        except Exception:
            pass

if __name__ == '__main__':
    main()