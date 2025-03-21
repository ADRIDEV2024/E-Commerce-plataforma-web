SSH_ENV=$HOME/.ssh/environment

function start_agent {
    echo "Initialising new SSH agent..."
    /usr/bin/ssh-agent | sed 's/^echo/#echo/' > ${SSH_ENV}
    chmod 600 ${SSH_ENV}
    . ${SSH_ENV} > /dev/null
    /usr/bin/ssh-add
    /usr/bin/ssh-add $HOME/.ssh/github
}

[[ -s ~/.bashrc ]] && source ~/.bashrc

if [ -f "${SSH_ENV}" ]; then
    . ${SSH_ENV} > /dev/null
    ps ${SSH_AGENT_PID} | grep ssh-agent$ > /dev/null || start_agent
else
    start_agent
fi
