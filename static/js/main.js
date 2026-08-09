// Lógica do frontend do controle de estoque

document.addEventListener('DOMContentLoaded', function () {
    destacarLinkAtivo();
    configurarBuscaTabelas();
    configurarFormularios();
    configurarFiltroHistorico();
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

// Exibe alerta visual ao enviar formulários
function configurarFormularios() {
    const formularios = document.querySelectorAll('.form-estoque');

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

// Aplica filtros combinados na tabela de histórico
function configurarFiltroHistorico() {
    const tabela = document.getElementById('tabelaHistorico');
    if (!tabela) return;

    const inputBusca = document.getElementById('buscaHistorico');
    const selectTipo = document.getElementById('filtroTipo');
    const inputDataInicio = document.getElementById('dataInicio');
    const inputDataFim = document.getElementById('dataFim');
    const btnFiltrar = document.getElementById('btnFiltrarHistorico');
    const btnLimpar = document.getElementById('btnLimparHistorico');

    function aplicarFiltros() {
        const termoBusca = inputBusca ? inputBusca.value.toLowerCase().trim() : '';
        const tipoSel = selectTipo ? selectTipo.value.toLowerCase() : 'todos';
        const dataInicioVal = inputDataInicio ? inputDataInicio.value : '';
        const dataFimVal = inputDataFim ? inputDataFim.value : '';

        const linhas = tabela.querySelectorAll('tbody tr');

        linhas.forEach(linha => {
            const colunas = linha.querySelectorAll('td');
            if (colunas.length < 6) return;

            const textoData = colunas[0].textContent.trim();
            const textoTipo = colunas[1].textContent.toLowerCase();
            const textoMaterial = colunas[2].textContent.toLowerCase();
            const textoResponsavel = colunas[4].textContent.toLowerCase();
            const textoObservacao = colunas[5].textContent.toLowerCase();

            let atendeBusca = true;
            if (termoBusca !== '') {
                const textoCompleto = `${textoMaterial} ${textoResponsavel} ${textoObservacao}`;
                atendeBusca = textoCompleto.includes(termoBusca);
            }

            let atendeTipo = true;
            if (tipoSel === 'entrada') {
                atendeTipo = textoTipo.includes('entrada');
            } else if (tipoSel === 'saida') {
                atendeTipo = textoTipo.includes('saída') || textoTipo.includes('saida');
            }

            let atendeData = true;
            if (dataInicioVal || dataFimVal) {
                const partesData = textoData.split(' ')[0].split('/');
                if (partesData.length === 3) {
                    const dataIso = `${partesData[2]}-${partesData[1].padStart(2, '0')}-${partesData[0].padStart(2, '0')}`;
                    
                    if (dataInicioVal && dataIso < dataInicioVal) {
                        atendeData = false;
                    }
                    if (dataFimVal && dataIso > dataFimVal) {
                        atendeData = false;
                    }
                }
            }

            if (atendeBusca && atendeTipo && atendeData) {
                linha.style.display = '';
            } else {
                linha.style.display = 'none';
            }
        });
    }

    if (btnFiltrar) {
        btnFiltrar.addEventListener('click', aplicarFiltros);
    }

    if (inputBusca) {
        inputBusca.addEventListener('keyup', function (e) {
            if (e.key === 'Enter') aplicarFiltros();
        });
    }

    if (selectTipo) {
        selectTipo.addEventListener('change', aplicarFiltros);
    }

    if (btnLimpar) {
        btnLimpar.addEventListener('click', function () {
            if (inputBusca) inputBusca.value = '';
            if (selectTipo) selectTipo.value = 'todos';
            if (inputDataInicio) inputDataInicio.value = '';
            if (inputDataFim) inputDataFim.value = '';
            aplicarFiltros();
        });
    }
}
