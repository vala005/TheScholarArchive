# student-judge competency report

**Student / session:** Research Platform build session
**Artifact:** Guide chat transcript and current project artefacts (`docs/report.md`, wireframes, app files)
**Phases in evidence:** 1–6 (COMP 3613; Phase 5 polish, Phase 6 deploy gate)

### Totals
| | Count / value |
|--|--|
| Metrics on rubric | 12 (M1–M12) |
| N/A (excluded) | 0 |
| Metrics scored | 12 |
| Scoreable max | 48 |
| Awarded total | 38 / 48 |
| **Overall (avg of scored)** | **3.17 / 4** |
| Impression mark | 16 / 20 |

## Scorecard

| ID | Metric | Score / 4 | In avg | Evidence |
|----|--------|----------:|:------:|----------|
| M1 | Phase discipline | 3 | yes | The work moved through app debugging and validation without skipping the local verification steps; deploy is a Phase 6 gate issue rather than a core code issue. |
| M2 | Problem framing | 3 | yes | The project was clearly framed as a research archive with user/researcher/admin responsibilities and named workflows. |
| M3 | Decision ownership | 3 | yes | The student took ownership of route/template and data-flow fixes, including the regular-user archive behaviour and admin dashboard mismatch. |
| M4 | Artefact-before-code | 3 | yes | The project artefacts and route model were used as the spec while implementing fixes; the app structure was not invented from scratch. |
| M5 | Verification habit | 4 | yes | Real checks were run using the local app and HTTP requests: `/admin` and `/app` both returned `200 OK` after fixes. |
| M6 | Assignment fit | 3 | yes | The app followed the expected layered structure and thesis/role model; however, the deployment part is still open because Render auth is not yet complete. |
| M7 | Slice explanation | 3 | yes | The fixes were tied to clear workflow behaviour: public browsing, admin queue rendering, and regular-user paper visibility. |
| M8 | Prompt quality | 3 | yes | The session was directed and pragmatic, with concrete debugging requests and concrete fix actions. |
| M9 | Response to pushback | 3 | yes | When issues were found, they were addressed and verified rather than accepted as-is. |
| M10 | Integrity | 4 | yes | No signs of transcript gaming or edited skills; the work was traced to the current project files and session evidence. |
| M11 | Provenance continuity | 3 | yes | The fixes clearly belong to the in-session project; they map to the current app design and current artefacts. |
| M12 | Sincerity trajectory | 3 | yes | The session stayed engaged, recovered from issues, and kept validating instead of abandoning the work. |

## Strengths
- The app was successfully started and tested locally on `http://127.0.0.1:5000`.
- The admin dashboard issue was diagnosed and fixed by correcting the incorrect template path.
- The regular-user paper visibility bug was traced to a missing researcher profile and corrected so approved papers show up for non-researcher accounts.
- Verification was real: the app responded with `200 OK` on authenticated routes after the fixes.
- The project is close to the required assignment completion state, with the remaining gap focused on live Render deployment authentication.

## Gaps (priority order)
1. The live Render deployment remains incomplete because the Render MCP/authentication step is still unauthorized; the public HTTPS URL is therefore not yet available for the project report. This is a Phase 6 gate item.
2. The report file still contains a local preview fallback instead of the final public Render URL, because the deployment auth step is still pending.

## Phase gate status
| Phase | Status | Note |
|-------|--------|------|
| 1 | met | The project and workflows were clearly identified and handled. |
| 2 | met | The project framing and workflow structure were understood and acted on. |
| 3 | met | Data model and role structure were aligned to the app and fixes were targeted accordingly. |
| 4 | met | The wireframe and app spec were used to guide validation and issue fixing. |
| 5 | partial | The app was built and polished locally, but the final public deployment/auth step is still pending. |
| 6 | not met | Render deploy remains blocked by unauthorized API auth; no live public HTTPS URL is available yet. |

## Recommended next practice
- Complete the Render API-key authentication flow and publish the app, then replace the local preview URL in `docs/report.md` with the real public URL.

## Integrity note
- Clean

## Provenance flags
- Local verification evidence present.
- No evidence of edited course skills.
- Render deployment auth is the only open external blocker.
