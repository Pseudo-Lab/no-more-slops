# Failure policy

| What happened | Record | Run | Tell the user |
| --- | --- | --- | --- |
| Output cut off at the token limit | Unreadable attempt (`incomplete: length`), scored wrong | Continue; repair it like any failed proposal | Count per method |
| Request or output blocked by a content filter (often HTTP 400 with a filter code) | Unreadable attempt with the filter reason; usage may be missing | Continue | Count; costs leave out or flag the unknown usage |
| Refusal or unparseable output | Unreadable attempt | Continue | Count |
| 401 / 403 | Error event | Stop | Key or permission for which service |
| 402 or a billing message | Error event | Stop; saved rows stay | Pay or raise the limit, then resume with the same settings |
| 404 / unknown deployment or model | Error event | Stop | The deployment or model name to fix |
| 408 / 429 / 5xx / timeout | Retry wait recorded | Bounded retries with backoff, then stop | Quota or provider status |
| Verifier returns no usable verdict | Error event | Stop; never invent a verdict | The response problem |
| Interrupted process | Nothing extra | Resume from the saved rows | That resuming continues where it stopped |

A route change after a failure (for example a gateway stops serving a model and
the provider is called directly) keeps the run valid only if the model and
questions are unchanged and the route is recorded from that attempt on.
Otherwise start a new run.
