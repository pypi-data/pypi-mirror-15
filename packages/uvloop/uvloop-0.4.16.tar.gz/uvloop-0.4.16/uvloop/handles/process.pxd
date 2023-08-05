cdef class UVProcess(UVHandle):
    cdef:
        object _returncode
        object _pid

        set _fds_to_close

        # Attributes used to compose uv_process_options_t:
        uv.uv_process_options_t options
        uv.uv_stdio_container_t[3] iocnt
        list __env
        char **uv_opt_env
        list __args
        char **uv_opt_args
        char *uv_opt_file
        bytes __cwd

    cdef _init(self, Loop loop, list args, dict env, cwd,
               start_new_session,
               stdin, stdout, stderr, pass_fds,
               debug_flags)

    cdef char** __to_cstring_array(self, list arr)
    cdef _init_args(self, list args)
    cdef _init_env(self, dict env)
    cdef _init_files(self, stdin, stdout, stderr)
    cdef _init_options(self, list args, dict env, cwd, start_new_session,
                       stdin, stdout, stderr)

    cdef _close_after_spawn(self, int fd)

    cdef _on_exit(self, int64_t exit_status, int term_signal)
    cdef _kill(self, int signum)


cdef class UVProcessTransport(UVProcess):
    cdef:
        list _exit_waiters
        list _init_futs
        bint _stdio_ready
        list _pending_calls
        object _protocol
        bint _finished

        WriteUnixTransport stdin
        ReadUnixTransport stdout
        ReadUnixTransport stderr

        object stdin_proto
        object stdout_proto
        object stderr_proto

    cdef _file_redirect_stdio(self, int fd)
    cdef _file_devnull(self)
    cdef _file_inpipe(self)
    cdef _file_outpipe(self)

    cdef _check_proc(self)
    cdef _pipe_connection_lost(self, int fd, exc)
    cdef _pipe_data_received(self, int fd, data)

    cdef _call_connection_made(self, waiter)
    cdef _try_finish(self)

    @staticmethod
    cdef UVProcessTransport new(Loop loop, protocol, args, env, cwd,
                                start_new_session,
                                stdin, stdout, stderr, pass_fds,
                                waiter,
                                debug_flags)
