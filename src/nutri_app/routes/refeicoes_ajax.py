from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime, date
from sqlalchemy import text
from src.nutri_app.database import engine
from src.nutri_app.utils.calorias_macros import (
    calcular_restantes_from_totais,
    buscar_metas_conn,
    calcular_totais_conn
)

refeicoes_ajax_bp = Blueprint('refeicoes_ajax', __name__)

@refeicoes_ajax_bp.route("/refeicoes/criar", methods=['POST'])
@login_required
def criar_refeicao():
    data = request.json
    alimento_id = data.get('alimento_id')
    porcao = data.get('porcao')
    tipo_refeicao = data.get('tipo_refeicao')

    if not alimento_id or not porcao or not tipo_refeicao:
        return jsonify({'erro': 'Dados incompletos'}), 400

    with engine.begin() as conn:
        usuario = conn.execute(text("""
            SELECT ultima_atualizacao
            FROM usuarios
            WHERE id = :id
        """), {"id": current_user.id}).mappings().first()

        hoje = date.today()
        if not usuario or not usuario["ultima_atualizacao"] or usuario["ultima_atualizacao"] != hoje:
            conn.execute(text("""
                UPDATE usuarios
                SET calorias_consumidas = 0,
                    proteinas_consumidas = 0,
                    carboidratos_consumidos = 0,
                    gorduras_consumidas = 0,
                    ultima_atualizacao = :hoje
                WHERE id = :id
            """), {"id": current_user.id, "hoje": hoje})
            
        query_catalogo = text("""
            SELECT id, nome, porcao, calorias, proteinas, carboidratos, gorduras
            FROM catalogo_alimentos
            WHERE id = :id
        """)
            
        alimento = conn.execute(query_catalogo, {"id": alimento_id}).mappings().first()

        if not alimento:
            return jsonify({'erro': 'Alimento não encontrado'}), 404

        fator = float(porcao) / float(alimento.porcao)
        calorias = round(float(alimento.calorias) * fator, 2)
        proteinas = round(float(alimento.proteinas) * fator, 2)
        carboidratos = round(float(alimento.carboidratos) * fator, 2)
        gorduras = round(float(alimento.gorduras) * fator, 2)

        data_refeicao = datetime.now().date()

        insert = text('''
            INSERT INTO refeicoes (usuario_id, catalogo_alimento_id, porcao, data, tipo_refeicao, calorias, proteinas, carboidratos, gorduras)
            VALUES (:usuario_id, :catalogo_alimento_id, :porcao, :data, :tipo_refeicao, :calorias, :proteinas, :carboidratos, :gorduras)
        ''')
        conn.execute(insert, {
            "usuario_id": current_user.id,
            "catalogo_alimento_id": alimento_id,
            "porcao": porcao,
            "data": data_refeicao,
            "tipo_refeicao": tipo_refeicao,
            "calorias": calorias,
            "proteinas": proteinas,
            "carboidratos": carboidratos,
            "gorduras": gorduras
        })

        update_user = text('''
            UPDATE usuarios
            SET calorias_consumidas = calorias_consumidas + :calorias,
                proteinas_consumidas = proteinas_consumidas + :proteinas,
                carboidratos_consumidos = carboidratos_consumidos + :carboidratos,
                gorduras_consumidas = gorduras_consumidas + :gorduras,
                ultima_atualizacao = :hoje
            WHERE id = :usuario_id
        ''')
        conn.execute(update_user, {
            "usuario_id": current_user.id,
            "calorias": calorias,
            "proteinas": proteinas,
            "carboidratos": carboidratos,
            "gorduras": gorduras,
            "hoje": hoje
        })
        
        totais = calcular_totais_conn(conn, current_user.id, data_refeicao)
        metas = buscar_metas_conn(conn, current_user.id)
        restantes = calcular_restantes_from_totais(metas, totais)
        
    return jsonify({'mensagem': 'Refeição registrada com sucesso', 'totais': totais, 'restantes': restantes})

@refeicoes_ajax_bp.route("/refeicoes/listar")
@login_required
def listar_refeicoes():
    data_refeicao = request.args.get("data")
    if not data_refeicao:
        data_refeicao = datetime.now().date()
    else:
        data_refeicao = datetime.strptime(data_refeicao, "%Y-%m-%d").date()

    tipos_fixos = ["Café da Manhã", "Almoço", "Jantar", "Lanche"]

    with engine.connect() as conn:
        query_refeicoes = text('''
            SELECT 
                r.id, 
                c.nome AS alimento,
                r.porcao, 
                r.calorias, 
                r.proteinas, 
                r.carboidratos, 
                r.gorduras,
                r.tipo_refeicao
            FROM refeicoes r
            LEFT JOIN catalogo_alimentos c ON r.catalogo_alimento_id = c.id
            WHERE r.usuario_id = :usuario_id 
              AND DATE(r.data) = :data_refeicao
            ORDER BY r.tipo_refeicao, r.id DESC
        ''')
        result = conn.execute(query_refeicoes, {
            "usuario_id": current_user.id,
            "data_refeicao": str(data_refeicao)
        })
        
        registros = [dict(row) for row in result.mappings()]
        
        totais = calcular_totais_conn(conn, current_user.id, data_refeicao)

        metas = buscar_metas_conn(conn, current_user.id)

        restantes = calcular_restantes_from_totais(metas, totais)
        
    refeicoes_por_tipo = {tipo: [] for tipo in tipos_fixos}
    for r in registros:
        tipo = r["tipo_refeicao"] or "Outros"
        if tipo not in refeicoes_por_tipo:
            refeicoes_por_tipo[tipo] = []
        refeicoes_por_tipo[tipo].append(r)
    
    return jsonify({
        "refeicoes": refeicoes_por_tipo,
        "totais": totais,
        "restantes": restantes
    })

@refeicoes_ajax_bp.route("/refeicoes/editar/<int:id>", methods=['PUT'])
@login_required
def editar_refeicao(id):
    data = request.json
    nova_porcao = data.get('porcao')
    novo_tipo_refeicao = data.get('tipo_refeicao')

    with engine.begin() as conn:
        select_query = text("""
            SELECT 
                r.*, 
                c.porcao AS porcao_padrao,
                c.calorias AS cal_a,
                c.proteinas AS prot_a,
                c.carboidratos AS carb_a,
                c.gorduras AS gord_a
            FROM refeicoes r
            LEFT JOIN catalogo_alimentos c ON r.catalogo_alimento_id = c.id
            WHERE r.id = :id AND r.usuario_id = :usuario_id
        """)

        refeicao = conn.execute(select_query, {
            "id": id,
            "usuario_id": current_user.id
        }).fetchone()

        if not refeicao:
            return jsonify({'erro': 'Refeição não encontrada'}), 404

        hoje = date.today()       
        conn.execute(text("""
            UPDATE usuarios
            SET calorias_consumidas = calorias_consumidas - :calorias,
                proteinas_consumidas = proteinas_consumidas - :proteinas,
                carboidratos_consumidos = carboidratos_consumidos - :carboidratos,
                gorduras_consumidas = gorduras_consumidas - :gorduras
            WHERE id = :usuario_id AND ultima_atualizacao = :hoje
        """), {
            "usuario_id": current_user.id,
            "hoje": hoje,
            "calorias": refeicao.calorias,
            "proteinas": refeicao.proteinas,
            "carboidratos": refeicao.carboidratos,
            "gorduras": refeicao.gorduras
        })
        
        fator = float(nova_porcao) / float(refeicao.porcao_padrao)
        calorias = round(float(refeicao.cal_a) * fator, 2)
        proteinas = round(float(refeicao.prot_a) * fator, 2)
        carboidratos = round(float(refeicao.carb_a) * fator, 2)
        gorduras = round(float(refeicao.gord_a) * fator, 2)

        update = text('''
            UPDATE refeicoes
            SET porcao = :porcao,
                tipo_refeicao = :tipo_refeicao,
                calorias = :calorias,
                proteinas = :proteinas,
                carboidratos = :carboidratos,
                gorduras = :gorduras
            WHERE id = :id AND usuario_id = :usuario_id
        ''')
        
        conn.execute(update, {
            "porcao": nova_porcao,
            "tipo_refeicao": novo_tipo_refeicao,
            "calorias": calorias,
            "proteinas": proteinas,
            "carboidratos": carboidratos,
            "gorduras": gorduras,
            "id": id,
            "usuario_id": current_user.id
        })

        conn.execute(text("""
            UPDATE usuarios
            SET calorias_consumidas = calorias_consumidas + :calorias,
                proteinas_consumidas = proteinas_consumidas + :proteinas,
                carboidratos_consumidos = carboidratos_consumidos + :carboidratos,
                gorduras_consumidas = gorduras_consumidas + :gorduras
            WHERE id = :usuario_id and ultima_atualizacao = :hoje
        """), {
            "usuario_id": current_user.id,
            "hoje": hoje,
            "calorias": calorias,
            "proteinas": proteinas,
            "carboidratos": carboidratos,
            "gorduras": gorduras
        })
        
        data_refeicao = datetime.now().date()
        totais = calcular_totais_conn(conn, current_user.id, data_refeicao)
        metas = buscar_metas_conn(conn, current_user.id)
        restantes = calcular_restantes_from_totais(metas, totais)
        
    return jsonify({'mensagem': 'Refeição atualizada com sucesso', 'totais': dict(totais), 'restantes': dict(restantes)})

@refeicoes_ajax_bp.route("/refeicoes/excluir/<int:id>", methods=['DELETE'])
@login_required
def excluir_refeicao(id):
    with engine.begin() as conn: 
        
        refeicao = conn.execute(text("""
            SELECT calorias, proteinas, carboidratos, gorduras
            FROM refeicoes
            WHERE id = :id AND usuario_id = :usuario_id
        """), {"id": id, "usuario_id": current_user.id}).mappings().first()

        if not refeicao:
            return jsonify({'erro': 'Refeição não encontrada'}), 404
        
        conn.execute(text("""
            UPDATE usuarios
            SET calorias_consumidas = calorias_consumidas - :calorias,
                proteinas_consumidas = proteinas_consumidas - :proteinas,
                carboidratos_consumidos = carboidratos_consumidos - :carboidratos,
                gorduras_consumidas = gorduras_consumidas - :gorduras
            WHERE id = :usuario_id
        """), {
            "usuario_id": current_user.id,
            "calorias": refeicao.calorias,
            "proteinas": refeicao.proteinas,
            "carboidratos": refeicao.carboidratos,
            "gorduras": refeicao.gorduras
        })
         
        delete = text("DELETE FROM refeicoes WHERE id = :id AND usuario_id = :usuario_id")
        conn.execute(delete, {
            "id": id,
            "usuario_id": current_user.id
        })

        totais = conn.execute(text("""
            SELECT calorias_consumidas, proteinas_consumidas, carboidratos_consumidos, gorduras_consumidas
            FROM usuarios
            WHERE id = :usuario_id
        """), {"usuario_id": current_user.id}).mappings().first()
        
        restantes = conn.execute(text("""
            SELECT calorias_restantes, proteinas_restantes, carboidratos_restantes, gorduras_restantes
            FROM usuarios
            WHERE id = :id
        """), {"id": current_user.id}).mappings().first()
        
    return jsonify({'mensagem': 'Refeição excluída com sucesso', 'totais': dict(totais), 'restantes': dict(restantes)})
