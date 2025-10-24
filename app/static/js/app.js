// Espera o HTML ser totalmente carregado para executar o script
document.addEventListener('DOMContentLoaded', () => {

    const taskList = document.getElementById('task-list');
    const addTaskForm = document.getElementById('add-task-form');
    const titleInput = document.getElementById('title');
    const descriptionInput = document.getElementById('description');

    // 1. FUNÇÃO PARA BUSCAR E EXIBIR AS TAREFAS
    async function fetchTasks() {
        // Faz a requisição GET para nossa API
        const response = await fetch('/api/tarefas');
        const tasks = await response.json();

        // Limpa a lista atual (o "Carregando...")
        taskList.innerHTML = '';

        if (tasks.length === 0) {
            taskList.innerHTML = '<p>Nenhuma tarefa encontrada. Adicione uma acima!</p>';
            return;
        }

        // Para cada tarefa retornada pela API, cria um elemento <li>
        tasks.forEach(task => {
            const li = document.createElement('li');
            li.innerHTML = `
                ${task.titulo} ${task.concluida ? '<strong>(Concluída)</strong>' : ''}
                &nbsp; | &nbsp;
                <button onclick="toggleTaskStatus(${task.id}, ${task.concluida})">
                    ${task.concluida ? 'Reabrir' : 'Concluir'}
                </button>
                &nbsp;
                <button onclick="deleteTask(${task.id})">Excluir</button>
            `;
            taskList.appendChild(li);
        });
    }

    // 2. FUNÇÃO PARA ADICIONAR UMA NOVA TAREFA
    addTaskForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Impede o recarregamento da página

        const title = titleInput.value;
        const description = descriptionInput.value;

        // Faz a requisição POST para nossa API
        await fetch('/api/tarefas', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ titulo: title, descricao: description }),
        });

        // Limpa os campos do formulário e atualiza a lista de tarefas
        titleInput.value = '';
        descriptionInput.value = '';
        fetchTasks();
    });

    // 3. FUNÇÃO PARA DELETAR UMA TAREFA
    window.deleteTask = async (taskId) => {
        if (confirm('Tem certeza que deseja excluir?')) {
            // Faz a requisição DELETE para nossa API
            await fetch(`/api/tarefas/${taskId}`, {
                method: 'DELETE',
            });
            // Atualiza a lista
            fetchTasks();
        }
    };

    // 4. FUNÇÃO PARA ATUALIZAR O STATUS (CONCLUIR/REABRIR)
    window.toggleTaskStatus = async (taskId, currentStatus) => {
        // Faz a requisição PUT para nossa API
        await fetch(`/api/tarefas/${taskId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ concluida: !currentStatus }), // Inverte o status atual
        });
        // Atualiza a lista
        fetchTasks();
    };

    // --- PONTO DE PARTIDA ---
    // Chama a função para buscar as tarefas assim que a página carrega
    fetchTasks();
});