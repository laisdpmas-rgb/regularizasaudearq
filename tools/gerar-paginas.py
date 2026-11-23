#!/usr/bin/env python3
"""Gera as páginas estratégicas (uma pasta com index.html por página) a partir do conteúdo abaixo.

Uso (na raiz do repositório):  python3 tools/gerar-paginas.py
O número de WhatsApp vem de assets/js/config.js (única fonte). Nada aqui é publicado por si só.
"""
import json, re
from html import escape
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
SITE = 'https://regularizasaudearq.com.br'
WA = re.search(r"whatsappNumber:\s*'(\d+)'", (ROOT / 'assets/js/config.js').read_text(encoding='utf-8')).group(1)
REVISADO = 'novembro de 2026'

AUTOR = ('Laís Abreu é arquiteta e urbanista, com pós-graduação lato sensu em Arquitetura Hospitalar pela '
         'Faculdade Israelita de Ciências da Saúde Albert Einstein (concluída em 2022), e atua no desenvolvimento de projetos arquitetônicos e documentação técnica para '
         'estabelecimentos de saúde.')

# Fontes oficiais efetivamente lidas (rótulo, URL)
F_MG = ('Governo de Minas Gerais: Solicitar avaliação de projeto arquitetônico', 'https://www.mg.gov.br/servico/solicitar-avaliacao-de-projeto-arquitetonico')
F_1002 = ('Anvisa: Perguntas & Respostas sobre a RDC 1002/2025 (1ª edição, 2026)', 'https://www.gov.br/anvisa/pt-br/assuntos/servicosdesaude/temas-em-destaque/PR__1002_2025_versao1_2026.pdf')
F_NT160 = ('Anvisa: Nota Técnica 160/2024 (cita a RDC 50/2002 e a RDC 51/2011 na avaliação de PBA)', 'https://www.gov.br/anvisa/pt-br/assuntos/servicosdesaude/novo-pac-saude/notas-tecnicas/nota-tecnica-160-2024')
F_CVS1 = ('Portaria CVS 1, de 9/1/2019 (Diário Oficial do Estado de SP, 31/01/2019)', 'https://ses.sp.bvs.br/wp-content/uploads/2021/09/E_PT-CVS-1_090119.pdf')
F_SP = ('Prefeitura de São Paulo: Laudo Técnico de Avaliação e DCFF', 'https://prefeitura.sp.gov.br/web/saude/w/vigilancia_em_saude/praca_de_atendimento/302055')
F_EST = ('Anvisa: Decisão nº 1, de 23/09/2026 (suspensão temporária da Nota Técnica 2/2024)', 'https://www.gov.br/anvisa/pt-br/assuntos/noticias-anvisa/2026/anvisa-suspende-temporariamente-nota-tecnica-sobre-servicos-de-estetica/sei_4496020_decisao.pdf/@@display-file/file')

def p(t): return f'<p>{t}</p>'
def ul(items): return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'
def ol(items): return '<ol>' + ''.join(f'<li>{i}</li>' for i in items) + '</ol>'

ATUACAO = ul([
    'Análise técnica preliminar da demanda, da atividade e do enquadramento, considerando CNAEs, imóvel e procedimentos realizados.',
    'Elaboração ou adequação do Projeto Básico de Arquitetura (PBA), quando aplicável.',
    'Memorial Descritivo Sanitário e Memorial de Atividades, conforme a necessidade do processo.',
    'Emissão de RRT referente aos serviços técnicos efetivamente contratados.',
    'Preparação da documentação técnica.',
    'Protocolo junto à Vigilância Sanitária e acompanhamento até a primeira manifestação do órgão, quando incluídos na contratação.',
])
FORA = p('<strong>O que não faz parte do serviço:</strong> execução ou gerenciamento de obras, decoração de interiores sem relação com o escopo sanitário e pagamento ou emissão de taxas públicas em nome do cliente. O Regulariza Saúde elabora o projeto e a documentação: a análise, a decisão e a licença são sempre da Vigilância Sanitária.')

PAGES = [
# ------------------------------------------------------------------ PBA
dict(
 id='pba', slug='projeto-basico-de-arquitetura-pba', track='click_cta_pba', crumb='Projeto Básico de Arquitetura (PBA)',
 title='Projeto Básico de Arquitetura (PBA) | Regulariza Saúde',
 desc='Elaboração de PBA, Memorial Descritivo Sanitário, RRT e documentação para Vigilância Sanitária de clínicas e consultórios. Solicite uma avaliação.',
 h1='Projeto Básico de Arquitetura (PBA) para Vigilância Sanitária',
 nugget='O Projeto Básico de Arquitetura (PBA) reúne os documentos técnicos de arquitetura — desenhos e memorial descritivo — que a Vigilância Sanitária pode pedir para avaliar a estrutura física, os ambientes e os fluxos de um estabelecimento de saúde. Se ele é exigido, e em que formato, varia conforme a atividade, o risco e o município ou estado.',
 cta1='Solicitar avaliação do meu projeto', cta_mid='Entenda o que seu estabelecimento precisa', cta_end='Solicitar avaliação do meu projeto',
 msg='Olá! Gostaria de uma avaliação e orçamento para elaboração de Projeto Básico de Arquitetura (PBA) para Vigilância Sanitária.\n\nCidade/UF: ',
 service='Projeto Básico de Arquitetura (PBA) para Vigilância Sanitária',
 service_desc='Elaboração ou adequação do Projeto Básico de Arquitetura, memoriais descritivos e documentação técnica para avaliação pela Vigilância Sanitária.',
 sections=[
  ('O que é o Projeto Básico de Arquitetura (PBA)?',
   p('É a documentação de projeto de arquitetura usada na avaliação de estabelecimentos de saúde pelo Sistema Nacional de Vigilância Sanitária. Ela mostra, de forma técnica, como o espaço será organizado: ambientes, circulações, fluxos, acabamentos e a descrição das atividades.')
   + p('Na prática, o conjunto costuma incluir o projeto arquitetônico (plantas) e um relatório técnico ou memorial descritivo. O portal do Governo de Minas Gerais, por exemplo, lista entre os documentos do pedido de avaliação o memorial descritivo (com os objetivos e as atividades do estabelecimento e a especificação básica dos materiais de acabamento), o projeto arquitetônico básico segundo as normas da ABNT e a ART ou o RRT do autor do projeto.')
   + p('A Anvisa cita a RDC 50/2002 e a RDC 51/2011 entre as normas usadas na avaliação de PBA. A RDC 51/2011 trata dos requisitos mínimos para a análise, avaliação e aprovação de projetos físicos de estabelecimentos de saúde no Sistema Nacional de Vigilância Sanitária, e a análise segue a legislação sanitária local.')),
  ('Quais estabelecimentos podem precisar de um PBA?',
   p('Dependendo da atividade, do risco e das regras locais, o PBA pode ser pedido para:')
   + ul(['clínicas médicas e consultórios;', 'clínicas e consultórios odontológicos;', 'serviços de estética, conforme os procedimentos realizados;', 'clínicas de vacinação;', 'laboratórios;', 'serviços de cirurgia ambulatorial;', 'Instituições de Longa Permanência para Idosos;', 'outros estabelecimentos assistenciais de saúde.'])
   + p('<strong>Isso não significa que todos precisam.</strong> A exigência de projeto depende do enquadramento sanitário da atividade e do procedimento da Vigilância Sanitária local. A própria RDC 51/2011 permite que os órgãos locais simplifiquem a análise para atividades de baixa complexidade. Em Minas Gerais, por exemplo, a aprovação do projeto pelo Estado se aplica a atividades de alto risco (nível de risco III), com algumas atividades dispensadas; a Vigilância Sanitária do município informa quem aprova o projeto no seu caso.')),
  ('O que está incluído na elaboração do PBA?', p('Cada contratação tem escopo definido por escrito. Os serviços que o Regulariza Saúde pode incluir são:') + ATUACAO + FORA, 'cta'),
  ('Qual a diferença entre projeto de interiores e projeto para Vigilância Sanitária?',
   p('Um projeto de interiores define estética, mobiliário e ambientação. Um projeto para Vigilância Sanitária é um documento técnico: demonstra que a atividade pretendida cabe no imóvel, com ambientes, fluxos, acessibilidade, acabamentos e instalações compatíveis com os requisitos sanitários aplicáveis.')
   + p('As duas atividades são complementares e cada uma exige conhecimentos próprios. Por isso, o projeto sanitário pode ser feito em parceria com o profissional que assina os interiores. A área da saúde tem normas e rotinas específicas (controle de infecção, fluxo de pacientes e de materiais), e é aí que o conhecimento específico em arquitetura da saúde faz diferença.')),
  ('Como funciona o atendimento remoto?',
   ol(['<strong>Primeiro contato.</strong> Você informa o tipo de estabelecimento, a cidade e a situação atual (vai abrir, já tem planta, recebeu exigência).',
       '<strong>Análise preliminar.</strong> Avaliamos a atividade, os CNAEs, o imóvel e os procedimentos para indicar o que provavelmente será necessário.',
       '<strong>Proposta.</strong> Você recebe o escopo, os entregáveis, as condições comerciais e o prazo de elaboração.',
       '<strong>Documentos.</strong> Você envia planta ou levantamento do imóvel, fotos, medidas, o contrato ou a matrícula, quando houver, e o relatório de exigências, se existir.',
       '<strong>Projeto e documentação.</strong> Elaboramos o PBA, os memoriais e o RRT, conforme o escopo contratado.',
       '<strong>Protocolo e acompanhamento.</strong> Quando contratados, protocolamos e acompanhamos até a primeira manifestação da Vigilância Sanitária.'])
   + p('<strong>Limitações do formato remoto:</strong> o trabalho depende de planta ou levantamento métrico confiável do imóvel e das diretrizes da Vigilância Sanitária local. Se os dados não estiverem confiáveis, indicamos o que precisa ser levantado antes de seguir.')),
 ],
 faq=[
  ('Toda clínica precisa de PBA?', 'Não necessariamente. A exigência depende do enquadramento da atividade (que considera o CNAE e os procedimentos realizados) e das regras da Vigilância Sanitária do município ou do estado. Por isso o primeiro passo é uma análise preliminar do seu caso.'),
  ('Quem pode elaborar um PBA?', 'É um projeto de arquitetura e engenharia, que deve ser assinado por profissional habilitado, com a responsabilidade técnica registrada em RRT (arquitetos, no CAU) ou ART (engenheiros, no CREA). Os órgãos de Minas Gerais e de São Paulo (capital) pedem esse registro. Confirme sempre a exigência da Vigilância Sanitária local.'),
  ('Posso utilizar a planta arquitetônica existente?', 'Em muitos casos a planta existente é o ponto de partida, mas ela precisa representar o imóvel como ele é e permitir mostrar os ambientes, fluxos e acabamentos que a análise sanitária considera. Na análise preliminar verificamos se ela serve como base ou se será preciso levantar o imóvel novamente.'),
  ('Quanto custa um projeto para Vigilância Sanitária?', 'Não existe valor único. O custo depende da área, da atividade e dos procedimentos, do estado da documentação, de quais serviços serão contratados (PBA, memoriais, RRT, protocolo, acompanhamento) e do município ou estado. Você recebe uma proposta por escrito depois da análise do caso. Taxas públicas, quando existirem, são separadas e pagas pelo próprio cliente.'),
  ('Quanto tempo demora o processo de aprovação?', 'São dois prazos distintos. O prazo de elaboração do projeto é combinado na proposta. O prazo de análise e a decisão pertencem à Vigilância Sanitária e variam por órgão. Nenhum profissional pode garantir aprovação, prazo de análise ou licença.'),
 ],
 related=[('LTA e avaliação físico-funcional em São Paulo', '/laudo-tecnico-de-avaliacao-lta-sao-paulo/'), ('Projeto para Vigilância Sanitária em Minas Gerais', '/projeto-arquitetonico-vigilancia-sanitaria-mg/'), ('Consultórios e clínicas odontológicas', '/projeto-vigilancia-sanitaria-consultorio-odontologico/'), ('Clínicas de estética', '/projeto-vigilancia-sanitaria-clinica-estetica/')],
 sources=[F_MG, F_NT160, F_1002],
),
# ------------------------------------------------------------------ LTA SP
dict(
 id='lta-sp', slug='laudo-tecnico-de-avaliacao-lta-sao-paulo', track='click_cta_lta', crumb='LTA em São Paulo',
 title='LTA para Vigilância Sanitária em São Paulo | Regulariza Saúde',
 desc='Projeto, documentação técnica e protocolo para a avaliação físico-funcional (LTA/DCFF) de estabelecimentos de saúde em São Paulo. Atendimento remoto.',
 h1='Laudo Técnico de Avaliação (LTA) para Vigilância Sanitária em São Paulo',
 nugget='No Estado de São Paulo, o Laudo Técnico de Avaliação (LTA) é a decisão da Vigilância Sanitária sobre a avaliação físico-funcional do projeto de uma edificação que abriga atividade de interesse da saúde. A Regulariza Saúde elabora o projeto e a documentação técnica e faz o protocolo do pedido; a emissão do LTA é sempre do órgão sanitário.',
 cta1='Solicitar orçamento do projeto para LTA/DCFF', cta_mid='Descubra quais documentos podem ser necessários', cta_end='Solicitar orçamento para LTA ou DCFF',
 msg='Olá! Preciso de orientação e orçamento para projeto, documentação e protocolo de LTA ou DCFF de um estabelecimento de saúde. Gostaria de entender os documentos e as etapas necessários.\n\nCidade/UF: ',
 service='Projeto, documentação técnica e protocolo para avaliação físico-funcional (LTA/DCFF)',
 service_desc='Elaboração do projeto arquitetônico, dos memoriais e do RRT, organização da documentação e protocolo do pedido de avaliação físico-funcional (LTA) ou de DCFF na Vigilância Sanitária, com atendimento remoto.',
 sections=[
  ('O que é o LTA e quando ele é necessário?',
   p('A Portaria CVS 1/2019, do Centro de Vigilância Sanitária de São Paulo, define o LTA como o “documento que expressa decisão do órgão de vigilância sanitária competente sobre a avaliação física funcional do projeto de edificação, e seus complementos, que abriga atividade de interesse da saúde”.')
   + p('A mesma portaria estabelece que os estabelecimentos sujeitos à avaliação físico-funcional do projeto devem atender à Portaria CVS 10/2017. Quais atividades estão sujeitas a essa avaliação depende do enquadramento e das regras do órgão sanitário do município: a lista é definida pela norma e pela Vigilância Sanitária local, e não por este site.')
   + p('<strong>Na capital paulista o documento é outro:</strong> veja a seção sobre a DCFF. Em outros municípios paulistas, confirme com a Vigilância Sanitária local qual documento se aplica.')),
  ('Na capital paulista, o LTA foi substituído pela DCFF',
   p('Segundo a Prefeitura de São Paulo, desde a Portaria SMS/COVISA 404/2024 (publicada em junho de 2024) o LTA foi substituído pela Declaração de Conformidade Físico Funcional (DCFF). Ela acompanha os pedidos de licença de funcionamento sanitária inicial, de alteração de endereço e de ampliação de atividades que alterem a estrutura física.')
   + p('Para o pedido, a Prefeitura lista a DCFF, a ART ou o RRT do profissional de engenharia ou arquitetura responsável pelo projeto físico e o Memorial Descritivo de Atividades. O Regulariza Saúde elabora o projeto, o RRT e os memoriais, organiza a documentação e faz o protocolo do pedido. Quem assina cada documento e como o envio é feito são confirmados com a Vigilância Sanitária antes de começar.')),
  ('Qual a diferença entre LTA e PBA?',
   p('<strong>São coisas diferentes e não são sinônimos.</strong> O LTA é uma decisão da Vigilância Sanitária. O Projeto Básico de Arquitetura (PBA) é um conjunto de documentos técnicos de projeto, elaborado por profissional habilitado. Em São Paulo, o projeto e os documentos técnicos são a base que o órgão sanitário avalia; o resultado dessa avaliação é o que o órgão formaliza.')
   + p('Cada órgão pode ter exigências próprias sobre a forma de apresentar o projeto. Por isso, a nomenclatura e os documentos pedidos devem ser confirmados no município do estabelecimento antes de começar.')),
  ('Quem emite o LTA e quem elabora o projeto e a documentação?',
   p('<strong>Quem emite o LTA</strong> é a Vigilância Sanitária competente. Nenhum arquiteto ou escritório emite o LTA nem pode antecipar o seu resultado.')
   + p('<strong>Quem elabora o projeto e a documentação técnica</strong> é um profissional habilitado, com responsabilidade técnica registrada em ART ou RRT. A Prefeitura de São Paulo, por exemplo, pede a ART ou o RRT do profissional de engenharia ou arquitetura responsável pelo projeto físico.')
   + p('O Regulariza Saúde atua nessa etapa: projeto arquitetônico, memoriais, RRT, organização da documentação e <strong>protocolo do pedido</strong> na Vigilância Sanitária.')),
  ('Atendimento remoto em todo o Brasil, com projetos em São Paulo',
   p('O atendimento é remoto e abrange o Brasil inteiro; esta página trata do Estado de São Paulo. Atendemos estabelecimentos em municípios paulistas como São Paulo, Campinas, Guarulhos, Barueri, Osasco, Jundiaí, Ribeirão Preto, São José do Rio Preto, Santos, São Bernardo do Campo e Sorocaba, entre outros.')
   + p('<strong>Os municípios não seguem, necessariamente, o mesmo fluxo de protocolo ou os mesmos documentos.</strong> A capital, por exemplo, adota a DCFF. Antes de começar, levantamos com a Vigilância Sanitária do seu município como o pedido deve ser feito.'), 'cta'),
  ('Quais documentos podem ser necessários?',
   p('Depende da atividade, do porte e do município. Na capital, os documentos da DCFF estão na seção acima. Nos demais municípios, eles seguem a portaria estadual e a orientação do órgão local.')
   + p('Além deles, normalmente precisamos de planta ou levantamento do imóvel, fotos e a descrição das atividades e procedimentos.')),
  ('Como funciona o trabalho até a primeira manifestação da VISA?',
   ol(['Análise preliminar da atividade, do imóvel e do município.', 'Proposta com escopo, entregáveis e condições comerciais.', 'Elaboração do projeto, dos memoriais e do RRT, conforme o escopo.', 'Organização da documentação e protocolo do pedido na Vigilância Sanitária.', 'Acompanhamento até a primeira manifestação do órgão sanitário, quando contratado.'])
   + p('A primeira manifestação, o prazo de análise e a decisão são da Vigilância Sanitária. O que acontece depois (novas rodadas de ajuste, por exemplo) é tratado conforme o que a proposta definir.') + FORA),
 ],
 faq=[
  ('Quem pode elaborar o LTA?', 'O LTA é emitido pela Vigilância Sanitária competente, e não elaborado por arquiteto ou engenheiro. O projeto e a documentação técnica que o órgão avalia são elaborados por profissional habilitado, com ART ou RRT.'),
  ('Quais documentos são necessários?', 'Depende da atividade e do município. Na capital, a Prefeitura de São Paulo lista a DCFF, a ART ou o RRT do responsável pelo projeto físico e o Memorial Descritivo de Atividades. Nos outros municípios, confirme com a Vigilância Sanitária local.'),
  ('Como solicitar a avaliação?', 'O pedido é feito junto à Vigilância Sanitária do município, pelo canal que ela definir. Nós preparamos o projeto e a documentação e fazemos o protocolo. Como o procedimento muda de município para município, levantamos o caminho correto antes de começar.'),
  ('Qual o prazo de análise?', 'O prazo de análise é do órgão sanitário e varia. Por isso, não prometemos prazos de aprovação. O prazo de elaboração do projeto é combinado na proposta.'),
  ('É necessário elaborar novo projeto para uma reforma?', 'Depende. Na capital paulista, a DCFF acompanha pedidos de ampliação de atividades que alterem a estrutura física do estabelecimento. Em outros municípios, a regra pode ser diferente. Em reformas, avaliamos o que muda no layout e nas atividades para indicar se é preciso apresentar projeto novo ou atualizado.'),
 ],
 related=[('Projeto Básico de Arquitetura (PBA)', '/projeto-basico-de-arquitetura-pba/'), ('Projeto para Vigilância Sanitária em Minas Gerais', '/projeto-arquitetonico-vigilancia-sanitaria-mg/')],
 sources=[F_CVS1, F_SP],
),
# ------------------------------------------------------------------ MG
dict(
 id='mg', slug='projeto-arquitetonico-vigilancia-sanitaria-mg', track='click_cta_mg', crumb='Vigilância Sanitária em Minas Gerais',
 title='Projeto para Vigilância Sanitária em MG | Regulariza Saúde',
 desc='Elaboração de projetos arquitetônicos e documentação para Vigilância Sanitária em Minas Gerais. Atendimento técnico para clínicas e consultórios.',
 h1='Projeto Arquitetônico para Vigilância Sanitária em Minas Gerais',
 nugget='Em Minas Gerais, a aprovação de projeto arquitetônico pela Vigilância Sanitária Estadual se aplica a estabelecimentos de alto risco (nível de risco III), com algumas atividades dispensadas. Quem aprova o projeto do seu estabelecimento é informado pela Vigilância Sanitária do município, e o pedido estadual é feito no sistema VISA Digital.',
 cta1='Solicitar avaliação para Minas Gerais', cta_mid='Solicite uma avaliação técnica', cta_end='Solicitar avaliação para Minas Gerais',
 msg='Olá! Tenho um estabelecimento de saúde em Minas Gerais e preciso de orientação sobre projeto arquitetônico e documentação para Vigilância Sanitária. Gostaria de avaliar meu caso.',
 service='Projeto arquitetônico e documentação para Vigilância Sanitária em Minas Gerais',
 service_desc='Elaboração de projeto arquitetônico, memoriais e documentação técnica para a Vigilância Sanitária em Minas Gerais.',
 sections=[
  ('Como funciona a análise de projetos pela Vigilância Sanitária em Minas Gerais?',
   p('Há três camadas de regras: as normas federais (como a RDC 50/2002 e a RDC 51/2011, da Anvisa), a legislação estadual e os procedimentos de cada Vigilância Sanitária municipal. O portal do Governo de Minas informa que a classificação de risco considera a atividade econômica (CNAE) e que, para atividades de nível de risco III em que a responsabilidade é do Estado, o projeto é aprovado pela Vigilância Sanitária Estadual.')
   + p('Algumas atividades são dispensadas dessa aprovação, conforme a Resolução SES/MG 10.601, de 21 de outubro de 2025. <strong>Para saber quem aprova o projeto do seu estabelecimento, a orientação oficial é procurar a Vigilância Sanitária do município.</strong>')),
  ('O que é o RAPA e quando ele é utilizado?',
   p('“RAPA” é o nome do módulo do sistema VISA Digital, da Secretaria de Estado de Saúde de Minas Gerais, usado para solicitar a avaliação de projeto arquitetônico (o manual oficial se chama “Manual VISA Digital Módulo RAPA”).')
   + p('Ele é usado quando a Vigilância Sanitária municipal orienta que o pedido de aprovação precisa ser feito junto à Vigilância Sanitária Estadual. O acesso exige conta no gov.br. <strong>Não é um procedimento obrigatório em todos os municípios nem para todos os estabelecimentos:</strong> depende do risco da atividade e do órgão responsável.')),
  ('Quais documentos podem ser necessários?',
   p('Segundo o portal do Governo de Minas, o pedido de avaliação de projeto arquitetônico pelo Estado reúne:')
   + ul(['relatório técnico ou memorial descritivo (objetivos e atividades, especificação básica dos acabamentos, descrição dos sistemas de ventilação mecânica e ar condicionado, quando previstos);', 'projeto arquitetônico básico de acordo com as normas da ABNT e com as leis e normas municipais, estaduais e federais;', 'memória de cálculo das áreas a adequar, reformar, construir ou ampliar, quando o estabelecimento não for isento da taxa de análise;', 'ART (CREA) ou RRT (CAU) de autoria do projeto, quitada;', 'Termo de Ciência do Proprietário e Termo de Responsabilidade Técnica, nos modelos da SES-MG.'])
   + p('A taxa de análise é gerada pelo próprio sistema e paga pelo requerente: ela não faz parte do serviço do Regulariza Saúde. Em processos municipais, a lista pode ser diferente.'), 'cta'),
  ('Atendimento em Belo Horizonte, Uberlândia e interior de Minas Gerais',
   p('O atendimento é remoto e cobre Belo Horizonte, Uberlândia e o interior de Minas Gerais. <strong>Os municípios não têm necessariamente procedimentos idênticos:</strong> alguns publicam formulários próprios e, em alguns casos, a análise é feita pelo órgão municipal. Antes de preparar a documentação, levantamos como o seu município conduz o processo.')
   + ATUACAO),
  ('Como funciona o acompanhamento até a primeira manifestação da VISA?',
   ol(['Análise preliminar do estabelecimento, da atividade (CNAE) e do município.', 'Definição de quem aprova o projeto, com base na orientação da Vigilância Sanitária municipal.', 'Elaboração do projeto, dos memoriais e do RRT.', 'Preparação da documentação e, quando contratado, protocolo.', 'Acompanhamento até a primeira manifestação do órgão sanitário, quando contratado.'])
   + p('O prazo de análise e a decisão são da Vigilância Sanitária. Novas rodadas de ajuste depois da primeira manifestação são tratadas conforme a proposta contratada.') + FORA),
 ],
 faq=[
  ('Como saber se minha clínica precisa apresentar projeto?', 'Pela classificação de risco da atividade (que considera o CNAE) e pela orientação da Vigilância Sanitária do seu município. A aprovação estadual de projeto se aplica a atividades de alto risco, com algumas dispensadas. Fazemos essa análise preliminar para o seu caso.'),
  ('O procedimento é municipal ou estadual?', 'Pode ser os dois. A Vigilância Sanitária municipal orienta se o pedido deve ir ao Estado; quando vai, é feito no VISA Digital. A inspeção e outras etapas do licenciamento podem permanecer com o município.'),
  ('O que é o RAPA?', 'É o módulo do sistema VISA Digital, da Secretaria de Estado de Saúde de Minas Gerais, para solicitar a avaliação de projeto arquitetônico. Não se aplica a todos os estabelecimentos nem a todos os municípios.'),
  ('Posso utilizar uma planta existente?', 'Em muitos casos ela é o ponto de partida, desde que represente o imóvel como ele é. O pedido exige projeto arquitetônico básico de acordo com as normas da ABNT e o memorial descritivo. Verificamos se a planta existente serve ou precisa ser refeita.'),
  ('O que acontece quando a Vigilância Sanitária solicita alterações?', 'O órgão pode pedir ajustes no projeto ou na documentação. Quando o acompanhamento está contratado, analisamos a manifestação e indicamos as adequações. Eventuais rodadas adicionais seguem as condições da proposta.'),
 ],
 related=[('Projeto Básico de Arquitetura (PBA)', '/projeto-basico-de-arquitetura-pba/'), ('Consultórios e clínicas odontológicas', '/projeto-vigilancia-sanitaria-consultorio-odontologico/'), ('Clínicas de estética', '/projeto-vigilancia-sanitaria-clinica-estetica/')],
 sources=[F_MG, F_NT160],
),
# ------------------------------------------------------------------ ODONTO
dict(
 id='odonto', slug='projeto-vigilancia-sanitaria-consultorio-odontologico', track='click_cta_odontologia', crumb='Consultórios odontológicos',
 title='Projeto para Vigilância Sanitária Odontológica | Regulariza Saúde',
 desc='Projeto arquitetônico e documentação para consultórios e clínicas odontológicas. Avaliação de processamento de materiais, fluxos e requisitos sanitários.',
 h1='Projeto Arquitetônico para Consultórios e Clínicas Odontológicas',
 nugget='A RDC 1002/2025, da Anvisa, passou a regular os serviços que prestam assistência odontológica e classifica os consultórios por estrutura física e equipamentos. Se um consultório precisa apresentar projeto à Vigilância Sanitária depende do enquadramento, da atividade e das regras do órgão local, e a análise preliminar mostra o que se aplica ao seu caso.',
 cta1='Solicitar avaliação do consultório odontológico', cta_mid='Entenda o que seu consultório precisa', cta_end='Solicitar avaliação do consultório odontológico',
 msg='Olá! Tenho um consultório/clínica odontológica e preciso de orientação sobre projeto arquitetônico e documentação para Vigilância Sanitária.',
 service='Projeto arquitetônico e documentação para consultórios e clínicas odontológicas',
 service_desc='Elaboração de projeto arquitetônico, memoriais e documentação técnica para consultórios e clínicas odontológicas, conforme a RDC 1002/2025 e as regras da Vigilância Sanitária local.',
 sections=[
  ('Quando um consultório odontológico precisa apresentar projeto à Vigilância Sanitária?',
   p('Depende do enquadramento da atividade, dos procedimentos realizados e das exigências da Vigilância Sanitária do município ou do estado. <strong>Não é uma regra única para todos os consultórios.</strong>')
   + p('A RDC 1002/2025, de 15 de dezembro de 2025, se aplica a todos os serviços que prestam assistência odontológica no país, públicos ou privados. Ela define classes de consultório (individual de classe I e de classe II, coletivo) e o centro cirúrgico odontológico, em função da estrutura física e dos equipamentos necessários à segurança do paciente. Em seu material de perguntas e respostas, a Anvisa lembra que a análise de projeto segue a legislação sanitária local (RDC 51/2011) e que o órgão local pode simplificar a avaliação para atividades de baixa complexidade.')),
  ('Quais aspectos técnicos merecem atenção em uma clínica odontológica?',
   p('Cada consultório tem uma realidade própria. Em geral, o projeto deve considerar:')
   + ul(['<strong>Processamento de produtos para saúde:</strong> onde e como os instrumentais são limpos, desinfetados ou esterilizados, e o fluxo unidirecional entre área suja e área limpa;', '<strong>Fluxos</strong> de pacientes, profissionais, materiais e resíduos;', '<strong>Ambiente de assistência</strong> e equipamentos, conforme a classe do consultório;', '<strong>Radiologia</strong>, quando houver equipamento de raio-X, com requisitos próprios de proteção radiológica;', '<strong>Acessibilidade</strong> e sanitários;', '<strong>Instalações e acabamentos</strong> adequados à limpeza.'])
   + p('Os ambientes e a estrutura mudam conforme a classe do consultório e os procedimentos. <strong>Não há um conjunto de ambientes obrigatório igual para todos</strong> e este site não publica metragens mínimas: elas dependem da norma aplicável ao seu caso e da orientação do órgão local.')),
  ('Processamento de materiais: como funciona a análise (a “CME odontológica”)?',
   p('Muitos profissionais chamam a área de limpeza e esterilização de “CME”. A Anvisa esclarece que a nomenclatura CME (Centro de Material e Esterilização) não se aplica à realidade ambulatorial dos serviços odontológicos: a RDC 1002/2025 fala em ambientes de processamento de produtos para saúde.')
   + p('A norma prevê três alternativas de estrutura: bancada setorizada exclusiva dentro da área de assistência, sala única e exclusiva para processamento, ou duas salas (suja e limpa). Consultórios coletivos e centros cirúrgicos odontológicos não podem usar a bancada setorizada. O serviço também pode terceirizar o processamento com empresa regularizada junto à autoridade sanitária, e nesse caso o protocolo precisa estar documentado.')
   + p('Na elaboração do projeto, verificamos qual alternativa é viável no seu imóvel e como demonstrá-la nas plantas e no memorial.'), 'cta'),
  ('Quais documentos são necessários?',
   p('Depende do órgão sanitário local. Em geral, o processo pode reunir o projeto arquitetônico, o memorial descritivo e de atividades, o RRT ou a ART do autor do projeto e os formulários do município ou do estado. Para consultórios já licenciados, a Anvisa informa que os serviços devem se adequar à RDC 1002/2025 no prazo de 360 dias contado da publicação da norma, inclusive quanto à estrutura física, salvo impossibilidades técnicas analisadas caso a caso. Confirme a data com a sua Vigilância Sanitária.')),
  ('Como o Regulariza Saúde pode ajudar?', ATUACAO + FORA),
 ],
 faq=[
  ('Consultório odontológico com uma cadeira precisa de projeto?', 'Depende da Vigilância Sanitária local. A RDC 1002/2025 se aplica a todo serviço que presta assistência odontológica, mas a exigência de apresentar projeto e o seu formato dependem do enquadramento e do órgão responsável. A análise preliminar indica o que se aplica ao seu caso.'),
  ('Como organizar o processamento de instrumentais?', 'A RDC 1002/2025 prevê bancada setorizada exclusiva na área de assistência, sala única exclusiva ou duas salas (suja e limpa). Consultórios coletivos e centros cirúrgicos odontológicos não podem usar a bancada. O processamento também pode ser terceirizado com empresa regularizada.'),
  ('É necessário ter expurgo?', 'A RDC 1002/2025 não impõe um modelo único. O que a norma exige é um fluxo organizado entre área suja e área limpa, dentro de uma das alternativas de estrutura de processamento. A escolha é feita pelo serviço, conforme sua demanda e a viabilidade do imóvel.'),
  ('Quais cuidados devem ser observados na sala de raio-X?', 'Se houver equipamento de raio-X, existem requisitos específicos de proteção radiológica, que dependem do equipamento e das normas aplicáveis, e devem ser confirmados com um profissional da área e com a Vigilância Sanitária. No projeto, a sala é prevista como ambiente próprio com localização e fluxos compatíveis.'),
  ('Posso reformar meu consultório sem apresentar novo projeto?', 'Depende. A Anvisa observa que a Vigilância Sanitária local pode dispensar a avaliação de um novo projeto, principalmente em adequações pequenas e de baixo risco sanitário, avaliadas caso a caso. Reformas que mudem fluxos, ambientes ou o tipo de atendimento costumam exigir avaliação.'),
 ],
 related=[('Projeto Básico de Arquitetura (PBA)', '/projeto-basico-de-arquitetura-pba/'), ('Clínicas de estética', '/projeto-vigilancia-sanitaria-clinica-estetica/')],
 sources=[F_1002, F_NT160],
),
# ------------------------------------------------------------------ ESTÉTICA
dict(
 id='estetica', slug='projeto-vigilancia-sanitaria-clinica-estetica', track='click_cta_estetica', crumb='Clínicas de estética',
 title='Projeto para Vigilância Sanitária de Clínicas de Estética',
 desc='Projetos arquitetônicos e documentação técnica para clínicas de estética. Avaliação conforme procedimentos realizados e exigências sanitárias.',
 h1='Projeto Arquitetônico para Clínicas de Estética e Procedimentos Estéticos',
 nugget='O enquadramento sanitário de uma clínica de estética depende dos procedimentos realizados, e o licenciamento e a inspeção são, em regra, das vigilâncias sanitárias estaduais, distrital e municipais. A Anvisa reavalia o tema desde setembro de 2026. Por isso, o primeiro passo é conferir os procedimentos e a posição do órgão local.',
 cta1='Solicitar avaliação da minha clínica de estética', cta_mid='Solicite uma avaliação técnica', cta_end='Solicitar avaliação da minha clínica de estética',
 msg='Olá! Tenho uma clínica de estética e gostaria de avaliar a necessidade de projeto arquitetônico e documentação para Vigilância Sanitária. Gostaria de informar os procedimentos realizados e receber orientação.',
 service='Projeto arquitetônico e documentação para clínicas de estética',
 service_desc='Elaboração de projeto arquitetônico, memoriais e documentação técnica para clínicas de estética, conforme os procedimentos realizados e as exigências da Vigilância Sanitária local.',
 sections=[
  ('Clínica de estética precisa de projeto para Vigilância Sanitária?',
   p('Depende dos procedimentos realizados e do entendimento da Vigilância Sanitária do seu município ou estado. <strong>Estabelecimentos de estética não têm, necessariamente, o mesmo enquadramento.</strong>')
   + p('A Nota Técnica 2/2024 da Anvisa distinguia serviços de saúde, que exigem execução ou supervisão por profissional de saúde habilitado, de serviços de interesse para a saúde, como estética e embelezamento, nos quais só poderiam ser usados produtos de aplicação externa regularizados. Em 23 de setembro de 2026, a Anvisa suspendeu temporariamente os efeitos dessa nota técnica, para reavaliar a matéria em grupo de trabalho. A decisão afirma que a suspensão não autoriza prática que a legislação veda e que as normas sanitárias vigentes continuam exigíveis.')
   + p('Na prática, procedimentos que envolvem produtos injetáveis, agulhas ou outros atos invasivos tendem a ser analisados com mais rigor pelas vigilâncias locais. Esse enquadramento é decidido caso a caso pelo órgão sanitário e deve ser conferido antes de investir em reforma ou projeto.')),
  ('Quais aspectos arquitetônicos devem ser avaliados?',
   p('Conforme a atividade, o projeto costuma tratar de:')
   + ul(['organização dos ambientes e separação de áreas;', 'lavatório para higienização das mãos;', 'fluxos de atendimento, de materiais e de resíduos;', 'limpeza e processamento de materiais, quando houver;', 'armazenamento de produtos e materiais;', 'descarte de resíduos e, quando aplicável, de perfurocortantes;', 'revestimentos e instalações compatíveis com a limpeza;', 'acessibilidade.'])
   + p('Quais desses itens são obrigatórios e como devem ser feitos depende do procedimento e do órgão local. Para serviços de saúde, a Anvisa cita, entre outras, a RDC 63/2011 (boas práticas de funcionamento) e a RDC 222/2018 (resíduos de serviços de saúde). Não generalizamos exigências: avaliamos o seu caso.')),
  ('Já abriu sua clínica e recebeu uma exigência da Vigilância Sanitária?',
   p('É comum. O primeiro passo é ler o relatório com calma e separar o que é ajuste de projeto do que é rotina do serviço (documentos, treinamentos, protocolos). Na parte arquitetônica, avaliamos a planta existente, comparamos com o que o órgão apontou e propomos as adequações necessárias, para que o projeto e a documentação respondam às exigências.')
   + p('A resposta, a análise e a decisão pertencem à Vigilância Sanitária, e não é possível garantir o resultado.'), 'cta'),
  ('Quais documentos podem ser necessários?',
   p('Dependem do enquadramento. Em geral, o processo pode reunir o projeto arquitetônico (quando exigido), o memorial descritivo e de atividades, o RRT do autor do projeto e os formulários do município ou do estado. Primeiro confirmamos com a Vigilância Sanitária local o que se aplica ao seu estabelecimento.')),
  ('Como funciona a contratação?',
   ol(['Você informa os procedimentos realizados, a cidade e a situação do imóvel.', 'Fazemos a análise preliminar do enquadramento e do espaço.', 'Você recebe a proposta com escopo, entregáveis, condições comerciais e prazo de elaboração.', 'Elaboramos o projeto e a documentação conforme o escopo.', 'Quando contratados, fazemos o protocolo e o acompanhamento até a primeira manifestação do órgão.']) + ATUACAO + FORA),
 ],
 faq=[
  ('Clínica de estética precisa de PBA?', 'Depende dos procedimentos e do órgão sanitário local. Não há uma resposta única para todas as clínicas de estética. A análise preliminar do seu caso indica se é preciso projeto e em que formato.'),
  ('Quais procedimentos alteram o enquadramento sanitário?', 'Quem decide é a Vigilância Sanitária do município ou do estado. Procedimentos com produtos injetáveis ou outros atos invasivos costumam ser tratados como atividade de saúde. A Anvisa reavalia o tema desde setembro de 2026, por isso confirme a posição do seu órgão local.'),
  ('Toda sala de procedimento precisa de pia?', 'Não existe resposta única. A necessidade e o tipo de lavatório dependem do procedimento e da exigência da Vigilância Sanitária. No projeto, avaliamos onde a higienização das mãos deve ficar, conforme os procedimentos informados.'),
  ('Coworking de estética precisa de projeto?', 'A Anvisa informa que o licenciamento sanitário é emitido para o serviço (a estrutura compartilhada) e não individualmente para cada profissional. A necessidade de projeto depende do enquadramento e do órgão local, e o projeto considera os ambientes e fluxos compartilhados.'),
  ('Como regularizar uma clínica que já está funcionando?', 'Começamos pelo diagnóstico: quais procedimentos são realizados, qual a situação da licença e o que o imóvel permite. Depois propomos as adequações e preparamos o projeto e a documentação exigidos pelo órgão local.'),
 ],
 related=[('Projeto Básico de Arquitetura (PBA)', '/projeto-basico-de-arquitetura-pba/'), ('Consultórios e clínicas odontológicas', '/projeto-vigilancia-sanitaria-consultorio-odontologico/')],
 sources=[F_EST, F_NT160, F_1002],
),
]

# ---------------------------------------------------------------------------------------------
def wa_url(msg): return f'https://wa.me/{WA}?text=' + quote(msg, safe='')

def wa_link(cls, label, pg, loc):
    return (f'<a class="{cls} whatsapp-link" href="{wa_url(pg["msg"])}" data-message="{escape(pg["msg"])}" '
            f'data-track="{pg["track"]}" data-cta-location="{loc}" target="_blank" rel="noopener noreferrer">{label}</a>')

HEADER = '''<header class="topbar"><div class="wrap nav"><a class="brand" href="/" aria-label="Regulariza Saúde — um serviço de Laís Abreu Arquitetura, início"><img class="brand-logo" src="/assets/logo/regulariza-saude-verde.svg" alt="" width="164" height="44"><span class="brand-by">Um serviço de<br>Laís Abreu Arquitetura</span></a><button class="menu-toggle" id="menuToggle" aria-expanded="false" aria-controls="navlinks" aria-label="Abrir menu">☰ Menu</button><nav class="navlinks" id="navlinks" aria-label="Navegação principal"><a href="/#servicos">Serviços</a><a href="/#parcerias">Para Arquitetos</a><a href="/#processo">Como funciona</a><a href="/#sobre">Sobre</a><a href="/#faq">Dúvidas frequentes</a><a class="btn btn-primary mobile-cta" href="#contato">Solicitar avaliação ↗</a></nav>{cta}</div></header>'''

FOOTER = '''<footer class="footer"><div class="wrap"><div class="footer-top"><div><a class="brand" href="/" aria-label="Regulariza Saúde — um serviço de Laís Abreu Arquitetura, início"><img class="brand-logo" src="/assets/logo/regulariza-saude-claro.svg" alt="" width="164" height="44" loading="lazy"><span class="brand-by">Um serviço de<br>Laís Abreu Arquitetura</span></a><p>Projetos arquitetônicos para regularização sanitária de estabelecimentos de saúde. Atendimento remoto em todo o Brasil.</p></div><nav class="footer-links" aria-label="Links do rodapé"><a href="/#servicos">Serviços</a><a href="/#parcerias">Para Arquitetos</a><a href="/#processo">Como funciona</a><a href="/#sobre">Sobre</a><a href="/#faq">Dúvidas frequentes</a></nav></div><nav class="footer-links footer-guides" aria-label="Guias"><a href="/projeto-basico-de-arquitetura-pba/">PBA</a><a href="/laudo-tecnico-de-avaliacao-lta-sao-paulo/">LTA em São Paulo</a><a href="/projeto-arquitetonico-vigilancia-sanitaria-mg/">Minas Gerais</a><a href="/projeto-vigilancia-sanitaria-consultorio-odontologico/">Odontologia</a><a href="/projeto-vigilancia-sanitaria-clinica-estetica/">Estética</a></nav><div class="footer-bottom"><span>© <span id="year"></span> Laís Abreu Arquitetura · Regulariza Saúde · CAU nº A263615-8</span><span>Contato via WhatsApp · <a href="/privacidade.html">Política de Privacidade</a></span></div></div></footer>'''

def jsonld(pg, url):
    graph = [
      {'@type': 'WebPage', '@id': url + '#pagina', 'url': url, 'name': pg['title'], 'description': pg['desc'], 'inLanguage': 'pt-BR',
       'isPartOf': {'@id': SITE + '/#negocio'}, 'about': {'@id': url + '#servico'}},
      {'@type': 'BreadcrumbList', '@id': url + '#trilha', 'itemListElement': [
         {'@type': 'ListItem', 'position': 1, 'name': 'Início', 'item': SITE + '/'},
         {'@type': 'ListItem', 'position': 2, 'name': pg['crumb'], 'item': url}]},
      {'@type': 'Service', '@id': url + '#servico', 'name': pg['service'], 'description': pg['service_desc'], 'url': url,
       'provider': {'@id': SITE + '/#negocio'}, 'areaServed': {'@type': 'Country', 'name': 'Brasil'}},
      {'@type': 'FAQPage', '@id': url + '#faq', 'mainEntity': [
         {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in pg['faq']]},
    ]
    return json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, separators=(',', ':'))

def render(pg):
    url = f'{SITE}/{pg["slug"]}/'
    secs = []
    for i, s in enumerate(pg['sections']):
        h2, body = s[0], s[1]
        secs.append(f'<section class="section prose-section"><div class="wrap"><div class="prose"><h2 class="serif">{h2}</h2>{body}</div></div></section>')
        if len(s) > 2 and s[2] == 'cta':
            secs.append(f'<section class="cta-band"><div class="wrap"><p class="cta-band-text">{pg["cta_mid"]}.</p>{wa_link("btn btn-accent", pg["cta_mid"] + " ↗", pg, "meio")}</div></section>')
    faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in pg['faq'])
    related = ''.join(f'<li><a href="{u}">{t}</a></li>' for t, u in pg['related'])
    sources = ''.join(f'<li><a href="{u}" rel="noopener" target="_blank">{t}</a></li>' for t, u in pg['sources'])
    return f'''<!doctype html>
<html lang="pt-BR" data-page="{pg['id']}">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(pg['title'])}</title>
  <meta name="description" content="{escape(pg['desc'])}">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <meta name="theme-color" content="#F3F0E8">
  <meta name="author" content="Laís Abreu Arquitetura">
  <meta property="og:locale" content="pt_BR"><meta property="og:type" content="website">
  <meta property="og:title" content="{escape(pg['title'])}"><meta property="og:description" content="{escape(pg['desc'])}">
  <meta property="og:url" content="{url}"><meta property="og:site_name" content="Regulariza Saúde ARQ">
  <meta property="og:image" content="{SITE}/assets/og-image.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Regulariza Saúde — arquitetura que viabiliza a saúde">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="icon" href="/favicon.ico" sizes="48x48">
  <link rel="preload" href="/assets/fonts/poppins-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/assets/fonts/source-sans-3-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/css/style.css">
  <script type="application/ld+json">{jsonld(pg, url)}</script>
</head>
<body>
<a class="skip-link" href="#conteudo">Pular para o conteúdo</a>
{HEADER.format(cta=wa_link("btn btn-primary whatsapp-link-header", "Solicitar avaliação ↗", pg, "cabecalho"))}
<main id="conteudo">
<section class="page-hero"><div class="wrap">
<nav class="crumbs" aria-label="Você está em"><ol><li><a href="/">Início</a></li><li aria-current="page">{pg['crumb']}</li></ol></nav>
<h1 class="serif">{pg['h1']}</h1>
<p class="nugget">{pg['nugget']}</p>
<div class="hero-actions">{wa_link("btn btn-accent", pg["cta1"] + " ↗", pg, "topo")}</div>
<p class="micro-note">Atendimento remoto para todo o Brasil, conforme a viabilidade técnica do caso.</p>
</div></section>
{''.join(secs)}
<section class="section prose-section" id="faq"><div class="wrap"><div class="prose"><h2 class="serif">Perguntas frequentes</h2><div class="faq-list">{faq}</div></div></div></section>
<section class="section prose-section"><div class="wrap"><div class="prose"><h2 class="serif">Quem assina o projeto</h2>{p(AUTOR)}<h3>Veja também</h3><ul class="related">{related}</ul><h3>Fontes oficiais consultadas</h3><ul class="sources">{sources}</ul>{p(f"Conteúdo informativo, revisado em {REVISADO}. As exigências variam conforme a atividade, o município e o estado e podem mudar: confirme sempre com a Vigilância Sanitária do seu município. Este texto não substitui a orientação do órgão sanitário nem garante aprovação, prazo ou licença.")}</div></div></section>
<section class="cta-section" id="contato"><div class="wrap cta-final"><h2 class="serif">Converse sobre a situação do seu projeto.</h2><p>Informe o tipo de estabelecimento, a cidade e a situação atual. Na primeira conversa entendemos o seu cenário, sem compromisso, para indicar o melhor caminho.</p>{wa_link("btn btn-accent", pg["cta_end"] + " ↗", pg, "final")}</div></section>
</main>
{FOOTER}
{wa_link("btn btn-primary floating-cta", "Solicitar avaliação ↗", pg, "flutuante").replace('<a ', '<a aria-label="Solicitar avaliação pelo WhatsApp" ', 1)}
<script src="/assets/js/config.js"></script><script src="/assets/js/track.js"></script><script src="/assets/js/page.js"></script>
</body>
</html>
'''

if __name__ == '__main__':
    for pg in PAGES:
        d = ROOT / pg['slug']; d.mkdir(exist_ok=True)
        (d / 'index.html').write_text(render(pg), encoding='utf-8')
        print('gerado', pg['slug'] + '/index.html')
