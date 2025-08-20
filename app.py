"""An streamlit app to operate YOKOGAWAGS200 to perform switch toggle.

It outputs voltage that raise and fall linearly bwtween 0 and v_max. 
1+, 2- option will output +v_max and -v_max.
"""
import streamlit as st
import json
import os
from utils import operate, connect, disconnect 


# Load config and initialized connection to false
CONFIG_FILE = "instruments.json"
with open(CONFIG_FILE, "r") as f:
    instruments = json.load(f)
if "initialized" not in st.session_state:
    for inst in instruments:
        inst["connected"] = False
    with open(CONFIG_FILE, "w") as f:
        json.dump(instruments, f, indent=4)
    st.session_state["initialized"] = True
st.title("Yoko Switch Control Panel")

# --- Add new instrument ---
new_address = st.text_input("Enter USB address")
if st.button("ADD"):
    if new_address and new_address not in [i["address"] for i in instruments]:
        instruments.append({
            "address": new_address,
            "v_max": 0.65,
            "rising_time": 0.2,
            "flat_time": 0.5,
            "connected": False, 
        })
        with open(CONFIG_FILE, "w") as f:
            json.dump(instruments, f, indent=4)
        st.rerun()
st.markdown("---")


for idx, inst in enumerate(instruments):
    # Show address with ✅ if connected
    display_address = inst['address'] + (" ✅" if inst.get("connected", False) else "")
    st.write(display_address)

    col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([1, 1.28, 0.1, 1.45, 1.45, 1.45, 0.1, 0.5, 0.5])

    # Delete button
    with col1:
        st.write("")  # push down
        if st.button("delete\ninst", key=f"delete_{idx}"):
            instruments.pop(idx)
            with open(CONFIG_FILE, "w") as f:
                json.dump(instruments, f, indent=4)
            st.rerun()

    # Connect / Disconnect button
    error_message = None
    with col2:
        st.write("")  # push down
        if not inst.get("connected", False):
            # Show connect button
            if st.button("connect\nto inst", key=f"connect_{idx}"):
                try:
                    if connect(inst['address']):
                        instruments[idx]["connected"] = True
                        with open(CONFIG_FILE, "w") as f:
                            json.dump(instruments, f, indent=4)
                        st.rerun()
                except Exception as e:
                    error_message = f"Error connecting {inst['address']}: {e}"
        else:
            # Show disconnect button
            if st.button("disconnect\nto inst", key=f"disconnect_{idx}"):
                try:
                    if disconnect(inst['address']):
                        instruments[idx]["connected"] = False
                        with open(CONFIG_FILE, "w") as f:
                            json.dump(instruments, f, indent=4)
                        st.rerun()
                except Exception as e:
                    error_message = f"Error disconnecting {inst['address']}: {e}"
    if error_message:
        st.error(error_message)

    # Vertical line
    with col3:
        st.markdown(
            """<div style="border-left: 2px solid #555; height: 90px; margin: 0px;"></div>""",
            unsafe_allow_html=True
        )

    # Parms
    with col4:
        v_max = st.number_input(f"|$V_{{max}}$| (Volt)", value=inst['v_max'], key=f"vmax_{idx}")
        inst['v_max'] = v_max   # update the dict
    with col5:
        rising_time = st.number_input("Rising Time (s)", value=inst['rising_time'], key=f"rising_time_{idx}")
        inst['rising_time'] = rising_time  # update the dict
    with col6:
        flat_time = st.number_input("Flat Time (s)", value=inst['flat_time'], key=f"flat_time_{idx}")
        inst['flat_time'] = flat_time  # update the dict


    # Vertical line
    with col7:
        st.markdown(
            """<div style="border-left: 2px solid #555; height: 90px; margin: 0px;"></div>""",
            unsafe_allow_html=True
        )

   # Operate buttons with full-width alert
    with col8:
        operate_plus = st.button("1+", key=f"plus_{idx}")
    with col9:
        operate_minus = st.button("2-", key=f"minus_{idx}")

    status_placeholder = st.empty()
    if operate_plus:
        if inst.get("connected", False):
            status_placeholder.warning("functioning 1+ operation...")
            operate(inst['address'], v_max, rising_time, flat_time, '+')
            status_placeholder.success(f"The inst with addr '{inst['address']}' has toggled the switch to 1+.")
        else:
            status_placeholder.warning(f"The inst with addr '{inst['address']}' is not connected!")

    if operate_minus:
        if inst.get("connected", False):
            status_placeholder.warning("functioning 2- operation...")
            operate(inst['address'], v_max, rising_time, flat_time, '-')
            status_placeholder.success(f"The inst with addr '{inst['address']}' has toggled the switch to 2-.")
        else:
            status_placeholder.warning(f"The inst with addr '{inst['address']}' is not connected!")
            
    st.markdown("---")

# Save updated values (including connected status)
with open(CONFIG_FILE, "w") as f:
    json.dump(instruments, f, indent=4)
