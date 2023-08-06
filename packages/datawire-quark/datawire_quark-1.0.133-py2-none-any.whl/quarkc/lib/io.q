quark *;

namespace quark {
    @doc("Promise-based I/O and scheduling APIs.")
    class IO {
        @doc("Send a HTTP request, get back Promise that gets HTTPResponse or HTTPError result.")
        Promise httpRequest(HTTPRequest request) {
        }

        @doc("Schedule a callable to run in the future, return Promise with its result.")
        Promise schedule(UnaryCallable callable, float delayInSeconds) {
        }

        /* For websockets:
           1. Figure out if all runtimes use same API path
           2. Write some toy sample code with proposed API to see if it improves things at all.
        */
    }
}
