# Practical notes still to be written

**Status 10 September 2026:** 22 of the 23 walkthrough steps and 5 of the 38 field cards carry a note. `n72-open` folds into the 72-hour fields step and needs none. The open field cards are open by choice.

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

## The slots — walkthrough steps


### `reg-role` — Phase 01 · Registration: Choose your role — **written**

Fields on this screen: **Role**


### `reg-csirt` — Phase 01 · Registration: Choose the CSIRT designated as coordinator — **written**

Fields on this screen: **CSIRT designated as coordinator**


### `reg-personal` — Phase 01 · Registration: Confirm your personal details — **written**

Fields on this screen: **First Name**, **Last Name**, **Email**, **Legal name (for legal entities)**


### `reg-manufacturer` — Phase 01 · Registration: Enter the manufacturer details — **written**

Fields on this screen: **Name**, **CSIRT Designated as Coordinator (CDaC)**, **Additional Information**


### `reg-invited` — Phase 01 · Registration: If you were invited: accept instead — **written**

Fields on this screen: **First Name**, **Last Name**, **Email**, **Legal name (for legal entities)**, and, on step 2 of 2, **Name / CDaC / Additional Information** pre-filled from the Primary AR


### `ew-start` — Phase 02 · Early Warning: Start the notification — **written**

No field table on this step — a note here would be about the screen or the flow.


### `ew-fields` — Phase 02 · Early Warning: Type, title, summary — **written**

Fields on this screen: **Notification Type (Vulnerability / Incident)** (1), **Title** (7), **Summary** (8)


### `ew-manufacturer` — Phase 02 · Early Warning: Pick the manufacturer — **written**

Fields on this screen: **Manufacturer** (9)


### `ew-submit` — Phase 02 · Early Warning: Submit, or save a draft — **written**

No field table on this step — a note here would be about the screen or the flow.


### `ew-validated` — Phase 02 · Early Warning: After the CSIRT validates — **written**

No field table on this step — a note here would be about the screen or the flow.


### `ew-notes` — Phase 02 · Early Warning: Additional notes, at any time — **written**

Fields on this screen: **AR Note**


### `n72-open` — Phase 03 · 72-hour notification: Reopen the notification

No field table on this step — a note here would be about the screen or the flow.


### `n72-fields` — Phase 03 · 72-hour notification: The fields that become mandatory now — **written**

Fields on this screen: **Considered sensitivity of information** (20), **Corrective or mitigating measures taken** (21), **Corrective or mitigating measures that user can take** (22), **General information** (v26), **General information about nature of incident** (i36), **Initial assessment of the incident** (i43)


### `pec-toggle` — Phase 03 · 72-hour notification: Only for a vulnerability: flag PEC — **written**

Fields on this screen: **Malicious actor that has exploited / is exploiting the vulnerability** (v31), **Particular Exceptional Circumstances (PEC)** (v32)


### `pec-reasons` — Phase 03 · 72-hour notification: Choose the ground, and say why — **written**

Fields on this screen: **PEC Delay Reason** (v33), **Please provide further information** (v34)


### `fin-open` — Phase 04 · Final Report: Reopen it one last time — **written**

No field table on this step — a note here would be about the screen or the flow.


### `fin-fields` — Phase 04 · Final Report: The closing fields — **written**

Fields on this screen: **Date when corrective or mitigating measure has been available** (v27), **Full description of the severity of the vulnerability** (v28), **Full description of the impact of the vulnerability** (v29), **Malicious actor that has exploited / is exploiting the vulnerability** (v31), **Applied and ongoing mitigation measures** (i37), **Detailed description of the Severity of the incident** (i38), **Detailed description of the Impact of the incident** (i39), **Type of threat or root cause that is likely to have triggered the incident** (i40)


### `role-invite` — Accounts and roles: Invite a Secondary AR — **written**

No field table — a note here would be about who to invite, and when.


### `role-claim` — Accounts and roles: Claim the Primary role — **written**

No field table — the succession question: who takes over, and how it is agreed in advance.


### `role-remove` — Accounts and roles: Remove an association — **written**

No field table — what to do before someone leaves.


### `role-addmfr` — Accounts and roles: Add another manufacturer — **written**

No field table — how it works when one AR represents several manufacturers.


### `role-details` — Accounts and roles: Check your details — **written**

No field table — what is worth checking, and when.


### `role-dashboard` — Accounts and roles: Watch the dashboard and the alerts — **written**

No field table — how you notice a deadline or an invalidated notification in time.


## Field slots — `Every field, explained`

Status at go-live, 10 September 2026: five cards carry a note (the measures fields and the two awareness dates); for the other 33 there was nothing from practice to add at this point, so they stay open by choice, not by omission.

One slot per field card, on top of the 23 walkthrough slots above. The
marker in the card header follows the content: write a note and **✱ From
practice** appears by itself. **⚑ Source note** marks the cards that already
carry a remark on ENISA’s text — those are the fields most likely to need a
practical note as well.

### Common fields

| Slot | Field | Already flagged |
|---|---|---|
| `field-1` | Notification type (Vulnerability/Incident) |  |
| `field-2` | Title |  |
| `field-3` | Summary |  |
| `field-4` | Manufacturer name |  |
| `field-5` | Member States where product available (Concerned CSIRT) |  |
| `field-6` | Product Name |  |
| `field-7` | Product version |  |
| `field-8` | Product Type (Default/Important/Critical) |  |
| `field-9` | Product Class |  |
| `field-10` | Product Category |  |
| `field-11` | End of support indicator | ⚑ source note |
| `field-12` | Component name |  |
| `field-13` | Mitigating measure expected shortly |  |
| `field-14` | User Action able to reduce impact |  |
| `field-15` | Considered sensitivity of information |  |
| `field-16` | Corrective or mitigating measures taken | — **written** |
| `field-17` | Corrective or mitigating measures users can take | ⚑ source note — **written** |
| `field-18` | Attack vector |  |

### Actively exploited vulnerability

| Slot | Field | Already flagged |
|---|---|---|
| `field-v19` | CVE ID |  |
| `field-v20` | EUVD ID |  |
| `field-v21` | General information |  |
| `field-v22` | Date when corrective or mitigating measure has been available |  |
| `field-v23` | Details about the security update/corrective measure available | new field, ENISA added it 10 Sep 2026 |
| `field-v24` | Full description of the severity of the vulnerability | ⚑ source note |
| `field-v25` | Full description of the impact of the vulnerability |  |
| `field-v26` | Date/time when you become aware of the Actively Exploited Vulnerability [1] | — **written** |
| `field-v27` | Malicious actor that has exploited/is exploiting the vulnerability |  |
| `field-v28` | Particular Exceptional Circumstances (PEC) | ⚑ source note |
| `field-v29` | PEC Delay Reason | ⚑ source note |
| `field-v30` | Please provide further information |  |

### Severe incident

| Slot | Field | Already flagged |
|---|---|---|
| `field-i31` | Incident is suspected of unlawful or malicious acts |  |
| `field-i32` | General information about nature of incident |  |
| `field-i33` | Applied or ongoing mitigation measures | ⚑ source note — **written** |
| `field-i34` | Detailed description of the Severity of the incident | ⚑ source note |
| `field-i35` | Detailed description of the Impact of the incident |  |
| `field-i36` | Type of Threat or root cause likely to have triggered incident |  |
| `field-i37` | Date/time when you become aware of the incident [2] | ⚑ source note — **written** |
| `field-i38` | Date/time incident occurred | ⚑ source note |
| `field-i39` | Initial assessment of the incident |  |
