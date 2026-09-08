# Practical notes still to be written

The walkthrough in `index.html` gives, for every screen: ENISA's screenshot, the
fields as that screen labels them, their status, and what ENISA says goes in
them. What it does not give is the part only you can write — what actually
trips people up, what a CSIRT wants to see, what you would tell a colleague
filling this in for the first time.

Each step below carries a marker in `index.html`. Search for it, and replace the
comment with a paragraph:

    <!-- OWN-NOTE ew-fields: your own practical note here, as <p class="ownnote">…</p> -->

becomes

    <p class="ownnote"><strong>From practice.</strong> …</p>

It renders as an accented block under the step, visibly yours rather than
ENISA's. Leave any marker untouched and nothing appears on the page — an empty
slot costs the reader nothing, so there is no need to fill them all, or in
order.

For a note about one field rather than the whole screen, the same paragraph
works: name the field in bold at the start.

## The slots


### `reg-role` — Phase 01 · Registration: Choose your role

Fields on this screen: **Role**


### `reg-csirt` — Phase 01 · Registration: Choose the CSIRT designated as coordinator

Fields on this screen: **CSIRT designated as coordinator**


### `reg-personal` — Phase 01 · Registration: Confirm your personal details

Fields on this screen: **First Name**, **Last Name**, **Email**, **Legal name (for legal entities)**


### `reg-manufacturer` — Phase 01 · Registration: Enter the manufacturer details

Fields on this screen: **Name**, **CSIRT Designated as Coordinator (CDaC)**, **Additional Information**


### `reg-invited` — Phase 01 · Registration: If you were invited: accept instead

No field table on this step — a note here would be about the screen or the flow.


### `ew-start` — Phase 02 · Early Warning: Start the notification

No field table on this step — a note here would be about the screen or the flow.


### `ew-fields` — Phase 02 · Early Warning: Type, title, summary

Fields on this screen: **Notification Type (Vulnerability / Incident)** (1), **Title** (7), **Summary** (8)


### `ew-manufacturer` — Phase 02 · Early Warning: Pick the manufacturer

Fields on this screen: **Manufacturer** (9)


### `ew-submit` — Phase 02 · Early Warning: Submit, or save a draft

No field table on this step — a note here would be about the screen or the flow.


### `ew-validated` — Phase 02 · Early Warning: After the CSIRT validates

No field table on this step — a note here would be about the screen or the flow.


### `ew-notes` — Phase 02 · Early Warning: Additional notes, at any time

Fields on this screen: **AR Note**


### `n72-open` — Phase 03 · 72-hour notification: Reopen the notification

No field table on this step — a note here would be about the screen or the flow.


### `n72-fields` — Phase 03 · 72-hour notification: The fields that become mandatory now

Fields on this screen: **Considered sensitivity of information** (20), **Corrective or mitigating measures taken** (21), **Corrective or mitigating measures that user can take** (22), **General information** (v26), **General information about nature of incident** (i36), **Initial assessment of the incident** (i43)


### `pec-toggle` — Phase 03 · 72-hour notification: Only for a vulnerability: flag PEC

Fields on this screen: **Malicious actor that has exploited / is exploiting the vulnerability** (v31), **Particular Exceptional Circumstances (PEC)** (v32)


### `pec-reasons` — Phase 03 · 72-hour notification: Choose the ground, and say why

Fields on this screen: **PEC Delay Reason** (v33), **Please provide further information** (v34)


### `fin-open` — Phase 04 · Final Report: Reopen it one last time

No field table on this step — a note here would be about the screen or the flow.


### `fin-fields` — Phase 04 · Final Report: The closing fields

Fields on this screen: **Date when corrective or mitigating measure has been available** (v27), **Full description of the severity of the vulnerability** (v28), **Full description of the impact of the vulnerability** (v29), **Malicious actor that has exploited / is exploiting the vulnerability** (v31), **Applied and ongoing mitigation measures** (i37), **Detailed description of the Severity of the incident** (i38), **Detailed description of the Impact of the incident** (I39), **Type of threat or root cause that is likely to have triggered the incident** (i40)
