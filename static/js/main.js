// Lógica do frontend do controle de estoque

document.addEventListener('DOMContentLoaded', function () {
    destacarLinkAtivo();
    configurarBuscaTabelas();
    configurarFormularios();
    configurarFiltroHistorico();
    carregarDashboard();
    configurarMateriais();
    configurarEntrada();
    configurarSaida();
    configurarConsultaEstoque();
});

// Marca a página atual no menu
function destacarLinkAtivo() {
    const paginaAtual = window.location.pathname.split('/').pop() || 'index.html';
    const links = document.querySelectorAll('.navbar-nav .nav-link');

    links.forEach(link => {
        const href = link.getAttribute('href');
        if (href === paginaAtual) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

// Filtra os registros da tabela ao digitar na busca
function configurarBuscaTabelas() {
    const inputsBusca = document.querySelectorAll('[data-busca-tabela]');

    inputsBusca.forEach(input => {
        const tabelaId = input.getAttribute('data-busca-tabela');
        const tabela = document.getElementById(tabelaId);

        if (!tabela) return;

        input.addEventListener('keyup', function () {
            const termo = this.value.toLowerCase().trim();
            const linhas = tabela.querySelectorAll('tbody tr');

            linhas.forEach(linha => {
                const textoLinha = linha.textContent.toLowerCase();
                if (textoLinha.includes(termo)) {
                    linha.style.display = '';
                } else {
                    linha.style.display = 'none';
                }
            });
        });
    });
}

// Confirma a exclusão do material
function confirmarExclusao(nomeItem) {
    const modalElemento = document.getElementById('modalConfirmarExclusao');
    if (!modalElemento) return;

    const spanNome = document.getElementById('nomeMaterialExcluir');
    if (spanNome) {
        spanNome.textContent = nomeItem;
    }

    const modal = new bootstrap.Modal(modalElemento);
    modal.show();
}

// Exibe alerta visual ao enviar formulários genéricos
function configurarFormularios() {
    const formularios = document.querySelectorAll('.form-estoque:not(#formNovoMaterial):not(#formEditarMaterial):not(#formEntrada):not(#formSaida)');

    formularios.forEach(form => {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            
            const alertaSucesso = document.getElementById('alertaSucessoForm');
            if (alertaSucesso) {
                alertaSucesso.classList.remove('d-none');
                setTimeout(() => {
                    alertaSucesso.classList.add('d-none');
                }, 4000);
            }

            this.reset();
        });
    });
}

// Carrega os dados reais do Dashboard consumindo GET /api/dashboard
async function carregarDashboard() {
    const elMateriais = document.getElementById('dashboard-materiais');
    const elTotal = document.getElementById('dashboard-total-itens');
    const elEstoqueBaixo = document.getElementById('dashboard-estoque-baixo');
    const elEntradas = document.getElementById('dashboard-entradas');
    const elSaidas = document.getElementById('dashboard-saidas');
    const tbodyMovimentacoes = document.getElementById('tabela-movimentacoes-recentes');

    if (!elMateriais && !tbodyMovimentacoes) return;

    try {
        const response = await fetch('/api/dashboard');
        if (!response.ok) {
            throw new Error(`Erro HTTP ao carregar dashboard: ${response.status}`);
        }

        const data = await response.json();
        const indicadores = data.indicadores || data;

        if (elMateriais) elMateriais.textContent = indicadores.materiais_cadastrados ?? 0;
        if (elTotal) elTotal.textContent = indicadores.total_itens != null ? Math.round(indicadores.total_itens).toLocaleString('pt-BR') : 0;
        if (elEstoqueBaixo) elEstoqueBaixo.textContent = indicadores.estoque_baixo ?? 0;
        if (elEntradas) elEntradas.textContent = indicadores.entradas_mes ?? 0;
        if (elSaidas) elSaidas.textContent = indicadores.saidas_mes ?? 0;

        if (tbodyMovimentacoes && Array.isArray(data.movimentacoes_recentes)) {
            tbodyMovimentacoes.innerHTML = '';

            if (data.movimentacoes_recentes.length === 0) {
                tbodyMovimentacoes.innerHTML = `
                    <tr>
                        <td colspan="6" class="text-center text-muted py-3">Nenhuma movimentação registrada.</td>
                    </tr>
                `;
                return;
            }

            data.movimentacoes_recentes.forEach(mov => {
                const tr = document.createElement('tr');

                const isEntrada = (mov.tipo || '').toLowerCase() === 'entrada';
                const badgeClass = isEntrada ? 'badge-tipo-entrada' : 'badge-tipo-saida';
                const badgeText = isEntrada ? 'Entrada' : 'Saída';

                const sinal = isEntrada ? '+' : '-';
                const unidade = mov.unidade_medida ? ` ${mov.unidade_medida}` : '';
                const quantidadeTexto = `${sinal} ${Math.round(mov.quantidade || 0)}${unidade}`;

                tr.innerHTML = `
                    <td>${mov.data_movimentacao || ''}</td>
                    <td><span class="badge ${badgeClass}">${badgeText}</span></td>
                    <td class="fw-semibold">${mov.material_nome || ''}</td>
                    <td>${quantidadeTexto}</td>
                    <td>${mov.responsavel || ''}</td>
                    <td>${mov.observacao || ''}</td>
                `;

                tbodyMovimentacoes.appendChild(tr);
            });
        }
    } catch (error) {
        console.error('Erro ao buscar dados do Dashboard via API:', error);
    }
}

// Configuração da página de Materiais
function configurarMateriais() {
    const tbody = document.getElementById('tbodyMateriais');
    if (!tbody) return;

    carregarMateriais();

    const formNovo = document.getElementById('formNovoMaterial');
    if (formNovo) {
        formNovo.addEventListener('submit', cadastrarMaterial);
    }

    const formEditar = document.getElementById('formEditarMaterial');
    if (formEditar) {
        formEditar.addEventListener('submit', salvarEdicaoMaterial);
    }

    const btnExcluir = document.getElementById('btnConfirmarExclusao');
    if (btnExcluir) {
        btnExcluir.addEventListener('click', excluirMaterial);
    }
}

function exibirMensagemMateriais(tipo, texto) {
    const elSucesso = document.getElementById('alertaSucessoMateriais');
    const txtSucesso = document.getElementById('textoSucessoMateriais');
    const elErro = document.getElementById('alertaErroMateriais');
    const txtErro = document.getElementById('textoErroMateriais');

    if (tipo === 'sucesso' && elSucesso && txtSucesso) {
        txtSucesso.textContent = texto;
        elSucesso.classList.remove('d-none');
        if (elErro) elErro.classList.add('d-none');
        setTimeout(() => elSucesso.classList.add('d-none'), 4000);
    } else if (tipo === 'erro' && elErro && txtErro) {
        txtErro.textContent = texto;
        elErro.classList.remove('d-none');
        if (elSucesso) elSucesso.classList.add('d-none');
    }
}

async function carregarMateriais() {
    const tbody = document.getElementById('tbodyMateriais');
    if (!tbody) return;

    try {
        const resposta = await fetch('/api/materiais');
        const dados = await resposta.json();

        if (!resposta.ok) {
            throw new Error(dados.erro || 'Não foi possível carregar a lista de materiais.');
        }

        tbody.innerHTML = '';

        if (!Array.isArray(dados) || dados.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="8" class="text-center text-muted py-3">Nenhum material encontrado.</td>
                </tr>
            `;
            return;
        }

        dados.forEach(material => {
            const tr = document.createElement('tr');

            const nomeEscapado = (material.nome || '').replace(/'/g, "\\'");

            tr.innerHTML = `
                <td class="fw-bold">${material.codigo || ''}</td>
                <td>${material.nome || ''}</td>
                <td>${material.categoria || ''}</td>
                <td>${material.unidade_medida || ''}</td>
                <td>${Math.round(material.quantidade || 0)}</td>
                <td>${Math.round(material.estoque_minimo || 0)}</td>
                <td>${material.localizacao || ''}</td>
                <td class="text-center">
                    <button class="btn btn-sm btn-outline-primary me-1" onclick="prepararEdicaoMaterial(${material.id})" title="Editar"><i class="bi bi-pencil"></i></button>
                    <button class="btn btn-sm btn-outline-danger" onclick="prepararExclusaoMaterial(${material.id}, '${nomeEscapado}')" title="Excluir"><i class="bi bi-trash"></i></button>
                </td>
            `;

            tbody.appendChild(tr);
        });

        const inputBusca = document.getElementById('buscaMaterial');
        if (inputBusca && inputBusca.value.trim() !== '') {
            inputBusca.dispatchEvent(new Event('keyup'));
        }
    } catch (erro) {
        console.error('Erro ao listar materiais:', erro);
        exibirMensagemMateriais('erro', erro.message);
    }
}

async function cadastrarMaterial(event) {
    event.preventDefault();

    const payload = {
        codigo: document.getElementById('codigoInput').value.trim(),
        nome: document.getElementById('nomeInput').value.trim(),
        categoria: document.getElementById('categoriaSelect').value,
        unidade_medida: document.getElementById('unidadeSelect').value,
        quantidade: parseFloat(document.getElementById('qtdInput').value) || 0,
        estoque_minimo: parseFloat(document.getElementById('estMinimoInput').value) || 0,
        localizacao: document.getElementById('localizacaoInput').value.trim()
    };

    try {
        const resposta = await fetch('/api/materiais', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const dados = await resposta.json();

        if (!resposta.ok) {
            throw new Error(dados.erro || 'Não foi possível cadastrar o material.');
        }

        const modalEl = document.getElementById('modalNovoMaterial');
        if (modalEl) {
            const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
            modal.hide();
        }

        event.target.reset();
        await carregarMateriais();
        exibirMensagemMateriais('sucesso', 'Material cadastrado com sucesso!');
    } catch (erro) {
        console.error('Erro ao cadastrar material:', erro);
        alert(erro.message);
    }
}

async function prepararEdicaoMaterial(id) {
    try {
        const resposta = await fetch(`/api/materiais/${id}`);
        const material = await resposta.json();

        if (!resposta.ok) {
            throw new Error(material.erro || 'Não foi possível carregar os dados do material para edição.');
        }

        document.getElementById('editIdInput').value = material.id;
        document.getElementById('editCodigoInput').value = material.codigo || '';
        document.getElementById('editNomeInput').value = material.nome || '';
        document.getElementById('editCategoriaSelect').value = material.categoria || '';
        document.getElementById('editUnidadeSelect').value = material.unidade_medida || '';
        document.getElementById('editQtdInput').value = material.quantidade ?? 0;
        document.getElementById('editEstMinimoInput').value = material.estoque_minimo ?? 0;
        document.getElementById('editLocalizacaoInput').value = material.localizacao || '';

        const modalEl = document.getElementById('modalEditarMaterial');
        if (modalEl) {
            const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
            modal.show();
        }
    } catch (erro) {
        console.error('Erro ao carregar material:', erro);
        exibirMensagemMateriais('erro', erro.message);
    }
}

async function salvarEdicaoMaterial(event) {
    event.preventDefault();

    const id = document.getElementById('editIdInput').value;
    if (!id) return;

    const payload = {
        codigo: document.getElementById('editCodigoInput').value.trim(),
        nome: document.getElementById('editNomeInput').value.trim(),
        categoria: document.getElementById('editCategoriaSelect').value,
        unidade_medida: document.getElementById('editUnidadeSelect').value,
        quantidade: parseFloat(document.getElementById('editQtdInput').value) || 0,
        estoque_minimo: parseFloat(document.getElementById('editEstMinimoInput').value) || 0,
        localizacao: document.getElementById('editLocalizacaoInput').value.trim()
    };

    try {
        const resposta = await fetch(`/api/materiais/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const dados = await resposta.json();

        if (!resposta.ok) {
            throw new Error(dados.erro || 'Não foi possível atualizar o material.');
        }

        const modalEl = document.getElementById('modalEditarMaterial');
        if (modalEl) {
            const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
            modal.hide();
        }

        await carregarMateriais();
        exibirMensagemMateriais('sucesso', 'Material atualizado com sucesso!');
    } catch (erro) {
        console.error('Erro ao atualizar material:', erro);
        alert(erro.message);
    }
}

function prepararExclusaoMaterial(id, nome) {
    const inputId = document.getElementById('deleteIdInput');
    const spanNome = document.getElementById('nomeMaterialExcluir');
    const alertaErro = document.getElementById('alertaErroExclusao');

    if (inputId) inputId.value = id;
    if (spanNome) spanNome.textContent = nome;
    if (alertaErro) {
        alertaErro.classList.add('d-none');
        alertaErro.textContent = '';
    }

    const modalEl = document.getElementById('modalConfirmarExclusao');
    if (modalEl) {
        const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
        modal.show();
    }
}

async function excluirMaterial() {
    const idInput = document.getElementById('deleteIdInput');
    if (!idInput || !idInput.value) return;

    const id = idInput.value;
    const alertaErro = document.getElementById('alertaErroExclusao');

    try {
        const resposta = await fetch(`/api/materiais/${id}`, {
            method: 'DELETE'
        });

        const dados = await resposta.json();

        if (!resposta.ok) {
            if (alertaErro) {
                alertaErro.textContent = dados.erro || 'Não foi possível excluir o material.';
                alertaErro.classList.remove('d-none');
            }
            return;
        }

        const modalEl = document.getElementById('modalConfirmarExclusao');
        if (modalEl) {
            const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
            modal.hide();
        }

        await carregarMateriais();
        exibirMensagemMateriais('sucesso', 'Material excluído com sucesso!');
    } catch (erro) {
        console.error('Erro ao excluir material:', erro);
        if (alertaErro) {
            alertaErro.textContent = erro.message;
            alertaErro.classList.remove('d-none');
        }
    }
}

// Helper para popular select de materiais
async function carregarSelectMateriais(selectId) {
    const select = document.getElementById(selectId);
    if (!select) return;

    try {
        const resposta = await fetch('/api/materiais');
        const dados = await resposta.json();

        if (!resposta.ok) return;

        const valAtual = select.value;
        select.innerHTML = '<option value="" selected disabled>Selecione um material...</option>';

        dados.forEach(m => {
            const opt = document.createElement('option');
            opt.value = m.id;
            opt.textContent = `${m.codigo} - ${m.nome} (${Math.round(m.quantidade)} ${m.unidade_medida} disponíveis)`;
            select.appendChild(opt);
        });

        if (valAtual) select.value = valAtual;
    } catch (e) {
        console.error('Erro ao carregar lista para select:', e);
    }
}

// Configuração da página de Entrada
function configurarEntrada() {
    const formEntrada = document.getElementById('formEntrada');
    if (!formEntrada) return;

    const dataInput = document.getElementById('dataInput');
    if (dataInput && !dataInput.value) {
        dataInput.value = new Date().toISOString().split('T')[0];
    }

    carregarSelectMateriais('materialSelect');
    carregarEntradasRecentes();

    formEntrada.addEventListener('submit', registrarEntrada);
}

async function carregarEntradasRecentes() {
    const tbody = document.getElementById('tbodyEntradasRecentes');
    if (!tbody) return;

    try {
        const resposta = await fetch('/api/movimentacoes?tipo=entrada');
        const dados = await resposta.json();

        if (!resposta.ok) throw new Error(dados.erro || 'Erro ao carregar entradas.');

        tbody.innerHTML = '';

        if (!Array.isArray(dados) || dados.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted py-3">Nenhuma entrada recente.</td></tr>';
            return;
        }

        dados.slice(0, 10).forEach(mov => {
            const tr = document.createElement('tr');
            const qty = Math.round(mov.quantidade || 0);
            const un = mov.unidade_medida ? ` ${mov.unidade_medida}` : '';

            tr.innerHTML = `
                <td>${mov.data_movimentacao || ''}</td>
                <td class="fw-semibold">${mov.material_nome || ''}</td>
                <td><span class="badge bg-success">+ ${qty}${un}</span></td>
                <td>${mov.responsavel || ''}</td>
                <td>${mov.observacao || ''}</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) {
        console.error('Erro ao carregar entradas recentes:', e);
    }
}

async function registrarEntrada(event) {
    event.preventDefault();

    const alertaSucesso = document.getElementById('alertaSucessoForm');
    const txtSucesso = document.getElementById('textoSucessoForm');
    const alertaErro = document.getElementById('alertaErroForm');
    const txtErro = document.getElementById('textoErroForm');

    const payload = {
        material_id: parseInt(document.getElementById('materialSelect').value),
        quantidade: parseFloat(document.getElementById('quantidadeInput').value) || 0,
        data_movimentacao: document.getElementById('dataInput').value,
        responsavel: document.getElementById('responsavelInput').value.trim(),
        observacao: document.getElementById('observacaoInput').value.trim()
    };

    try {
        const resposta = await fetch('/api/movimentacoes/entrada', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const dados = await resposta.json();

        if (!resposta.ok) {
            throw new Error(dados.erro || 'Não foi possível registrar a entrada.');
        }

        if (alertaErro) alertaErro.classList.add('d-none');
        if (txtSucesso) txtSucesso.textContent = dados.mensagem || 'Entrada registrada com sucesso.';
        if (alertaSucesso) {
            alertaSucesso.classList.remove('d-none');
            setTimeout(() => alertaSucesso.classList.add('d-none'), 4000);
        }

        event.target.reset();
        const dataInput = document.getElementById('dataInput');
        if (dataInput) dataInput.value = new Date().toISOString().split('T')[0];

        carregarSelectMateriais('materialSelect');
        carregarEntradasRecentes();
    } catch (erro) {
        console.error('Erro ao registrar entrada:', erro);
        if (alertaSucesso) alertaSucesso.classList.add('d-none');
        if (txtErro) txtErro.textContent = erro.message;
        if (alertaErro) alertaErro.classList.remove('d-none');
    }
}

// Configuração da página de Saída
function configurarSaida() {
    const formSaida = document.getElementById('formSaida');
    if (!formSaida) return;

    const dataSaidaInput = document.getElementById('dataSaidaInput');
    if (dataSaidaInput && !dataSaidaInput.value) {
        dataSaidaInput.value = new Date().toISOString().split('T')[0];
    }

    carregarSelectMateriais('materialSelectSaida');
    carregarSaidasRecentes();

    formSaida.addEventListener('submit', registrarSaida);
}

async function carregarSaidasRecentes() {
    const tbody = document.getElementById('tbodySaidasRecentes');
    if (!tbody) return;

    try {
        const resposta = await fetch('/api/movimentacoes?tipo=saida');
        const dados = await resposta.json();

        if (!resposta.ok) throw new Error(dados.erro || 'Erro ao carregar saídas.');

        tbody.innerHTML = '';

        if (!Array.isArray(dados) || dados.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted py-3">Nenhuma saída recente.</td></tr>';
            return;
        }

        dados.slice(0, 10).forEach(mov => {
            const tr = document.createElement('tr');
            const qty = Math.round(mov.quantidade || 0);
            const un = mov.unidade_medida ? ` ${mov.unidade_medida}` : '';

            tr.innerHTML = `
                <td>${mov.data_movimentacao || ''}</td>
                <td class="fw-semibold">${mov.material_nome || ''}</td>
                <td><span class="badge bg-secondary">- ${qty}${un}</span></td>
                <td>${mov.responsavel || ''}</td>
                <td>${mov.destino || ''}</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) {
        console.error('Erro ao carregar saídas recentes:', e);
    }
}

async function registrarSaida(event) {
    event.preventDefault();

    const alertaSucesso = document.getElementById('alertaSucessoForm');
    const txtSucesso = document.getElementById('textoSucessoForm');
    const alertaErro = document.getElementById('alertaErroForm');
    const txtErro = document.getElementById('textoErroForm');

    const payload = {
        material_id: parseInt(document.getElementById('materialSelectSaida').value),
        quantidade: parseFloat(document.getElementById('qtdSaidaInput').value) || 0,
        data_movimentacao: document.getElementById('dataSaidaInput').value,
        responsavel: document.getElementById('responsavelSaidaInput').value.trim(),
        destino: document.getElementById('destinoInput').value.trim(),
        observacao: document.getElementById('obsSaidaInput').value.trim()
    };

    try {
        const resposta = await fetch('/api/movimentacoes/saida', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const dados = await resposta.json();

        if (!resposta.ok) {
            throw new Error(dados.erro || 'Não foi possível registrar a saída.');
        }

        if (alertaErro) alertaErro.classList.add('d-none');
        if (txtSucesso) txtSucesso.textContent = dados.mensagem || 'Saída registrada com sucesso.';
        if (alertaSucesso) {
            alertaSucesso.classList.remove('d-none');
            setTimeout(() => alertaSucesso.classList.add('d-none'), 4000);
        }

        event.target.reset();
        const dataSaidaInput = document.getElementById('dataSaidaInput');
        if (dataSaidaInput) dataSaidaInput.value = new Date().toISOString().split('T')[0];

        carregarSelectMateriais('materialSelectSaida');
        carregarSaidasRecentes();
    } catch (erro) {
        console.error('Erro ao registrar saída:', erro);
        if (alertaSucesso) alertaSucesso.classList.add('d-none');
        if (txtErro) txtErro.textContent = erro.message;
        if (alertaErro) alertaErro.classList.remove('d-none');
    }
}

// Configuração da página Consulta de Estoque
function configurarConsultaEstoque() {
    const tbody = document.getElementById('tbodyConsultaEstoque');
    if (!tbody) return;

    carregarConsultaEstoque();
}

async function carregarConsultaEstoque() {
    const tbody = document.getElementById('tbodyConsultaEstoque');
    if (!tbody) return;

    try {
        const resposta = await fetch('/api/materiais');
        const dados = await resposta.json();

        if (!resposta.ok) throw new Error(dados.erro || 'Erro ao carregar consulta de estoque.');

        tbody.innerHTML = '';

        if (!Array.isArray(dados) || dados.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted py-3">Nenhum material cadastrado.</td></tr>';
            return;
        }

        dados.forEach(material => {
            const tr = document.createElement('tr');
            const qtd = Math.round(material.quantidade || 0);
            const estMin = Math.round(material.estoque_minimo || 0);

            let corQtd = 'text-success';
            let badgeSituacao = '<span class="badge badge-estoque-normal"><i class="bi bi-check-lg me-1"></i> Normal</span>';

            if (qtd === 0) {
                corQtd = 'text-danger';
                badgeSituacao = '<span class="badge badge-sem-estoque"><i class="bi bi-x-lg me-1"></i> Sem Estoque</span>';
            } else if (qtd <= estMin) {
                corQtd = 'text-warning';
                badgeSituacao = '<span class="badge badge-estoque-baixo"><i class="bi bi-exclamation-triangle me-1"></i> Estoque Baixo</span>';
            }

            tr.innerHTML = `
                <td class="fw-bold">${material.codigo || ''}</td>
                <td class="fw-semibold">${material.nome || ''}</td>
                <td>${material.categoria || ''}</td>
                <td class="fw-bold ${corQtd}">${qtd}</td>
                <td>${material.unidade_medida || ''}</td>
                <td>${estMin}</td>
                <td>${badgeSituacao}</td>
                <td>${material.localizacao || ''}</td>
            `;

            tbody.appendChild(tr);
        });

        const inputBusca = document.getElementById('buscaEstoque');
        if (inputBusca && inputBusca.value.trim() !== '') {
            inputBusca.dispatchEvent(new Event('keyup'));
        }
    } catch (e) {
        console.error('Erro ao consultar estoque:', e);
    }
}

// Configuração da página de Histórico
function configurarFiltroHistorico() {
    const tabela = document.getElementById('tabelaHistorico');
    if (!tabela) return;

    const inputBusca = document.getElementById('buscaHistorico');
    const selectTipo = document.getElementById('filtroTipo');
    const inputDataInicio = document.getElementById('dataInicio');
    const inputDataFim = document.getElementById('dataFim');
    const btnFiltrar = document.getElementById('btnFiltrarHistorico');
    const btnLimpar = document.getElementById('btnLimparHistorico');

    async function buscarEExibirHistorico() {
        const tbody = document.getElementById('tbodyHistorico');
        if (!tbody) return;

        const buscaVal = inputBusca ? inputBusca.value.trim() : '';
        const tipoVal = selectTipo ? selectTipo.value : 'todos';
        const inicioVal = inputDataInicio ? inputDataInicio.value : '';
        const fimVal = inputDataFim ? inputDataFim.value : '';

        const params = new URLSearchParams();
        if (buscaVal) params.append('busca', buscaVal);
        if (tipoVal && tipoVal !== 'todos') params.append('tipo', tipoVal);
        if (inicioVal) params.append('data_inicio', inicioVal);
        if (fimVal) params.append('data_fim', fimVal);

        try {
            const resposta = await fetch(`/api/movimentacoes?${params.toString()}`);
            const dados = await resposta.json();

            if (!resposta.ok) throw new Error(dados.erro || 'Erro ao filtrar histórico.');

            tbody.innerHTML = '';

            if (!Array.isArray(dados) || dados.length === 0) {
                tbody.innerHTML = '<tr><td colspan="6" class="text-center text-muted py-3">Nenhuma movimentação encontrada.</td></tr>';
                return;
            }

            dados.forEach(mov => {
                const tr = document.createElement('tr');
                const isEntrada = (mov.tipo || '').toLowerCase() === 'entrada';
                const badgeClass = isEntrada ? 'badge-tipo-entrada' : 'badge-tipo-saida';
                const badgeIcon = isEntrada ? 'bi-arrow-down-circle' : 'bi-arrow-up-circle';
                const badgeText = isEntrada ? 'Entrada' : 'Saída';
                const textCor = isEntrada ? 'text-success' : 'text-secondary';

                const sinal = isEntrada ? '+' : '-';
                const unidade = mov.unidade_medida ? ` ${mov.unidade_medida}` : '';
                const quantidadeTexto = `${sinal} ${Math.round(mov.quantidade || 0)}${unidade}`;

                let obsDestino = mov.observacao || '';
                if (mov.destino) {
                    obsDestino += obsDestino ? ` (${mov.destino})` : mov.destino;
                }

                tr.innerHTML = `
                    <td>${mov.data_movimentacao || ''}</td>
                    <td><span class="badge ${badgeClass}"><i class="bi ${badgeIcon} me-1"></i> ${badgeText}</span></td>
                    <td class="fw-semibold">${mov.material_nome || ''}</td>
                    <td class="fw-bold ${textCor}">${quantidadeTexto}</td>
                    <td>${mov.responsavel || ''}</td>
                    <td>${obsDestino}</td>
                `;

                tbody.appendChild(tr);
            });
        } catch (e) {
            console.error('Erro ao buscar histórico:', e);
        }
    }

    // Carrega histórico inicial
    buscarEExibirHistorico();

    if (btnFiltrar) {
        btnFiltrar.addEventListener('click', buscarEExibirHistorico);
    }

    if (inputBusca) {
        inputBusca.addEventListener('keyup', function (e) {
            if (e.key === 'Enter') buscarEExibirHistorico();
        });
    }

    if (selectTipo) {
        selectTipo.addEventListener('change', buscarEExibirHistorico);
    }

    if (btnLimpar) {
        btnLimpar.addEventListener('click', function () {
            if (inputBusca) inputBusca.value = '';
            if (selectTipo) selectTipo.value = 'todos';
            if (inputDataInicio) inputDataInicio.value = '';
            if (inputDataFim) inputDataFim.value = '';
            buscarEExibirHistorico();
        });
    }
}
