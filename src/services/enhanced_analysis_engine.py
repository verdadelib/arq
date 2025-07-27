#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Enhanced Analysis Engine
Motor de análise avançado com múltiplas IAs e sistemas integrados
"""

import os
import logging
import time
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from services.gemini_client import gemini_client
from services.websailor_integration import websailor_agent
from services.deep_search_service import deep_search_service

logger = logging.getLogger(__name__)

class EnhancedAnalysisEngine:
    """Motor de análise avançado com integração de múltiplos sistemas"""
    
    def __init__(self):
        """Inicializa o motor de análise"""
        self.max_analysis_time = 1800  # 30 minutos
        self.systems_enabled = {
            'gemini': bool(gemini_client),
            'websailor': websailor_agent.is_available(),
            'deep_search': bool(deep_search_service)
        }
        
        logger.info(f"Enhanced Analysis Engine inicializado - Sistemas: {self.systems_enabled}")
    
    def generate_comprehensive_analysis(
        self, 
        data: Dict[str, Any],
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Gera análise abrangente usando todos os sistemas disponíveis"""
        
        start_time = time.time()
        logger.info(f"🚀 Iniciando análise abrangente para {data.get('segmento')}")
        
        try:
            # FASE 1: Coleta de dados
            logger.info("📊 FASE 1: Coleta de dados...")
            research_data = self._collect_research_data(data, session_id)
            
            # FASE 2: Análise com IA
            logger.info("🧠 FASE 2: Análise com IA...")
            ai_analysis = self._perform_ai_analysis(data, research_data)
            
            # FASE 3: Consolidação final
            logger.info("🎯 FASE 3: Consolidação final...")
            final_analysis = self._consolidate_analysis(data, research_data, ai_analysis)
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            # Adiciona metadados
            final_analysis["metadata"] = {
                "processing_time_seconds": processing_time,
                "processing_time_formatted": f"{int(processing_time // 60)}m {int(processing_time % 60)}s",
                "analysis_engine": "ARQV30 Enhanced v2.0",
                "systems_used": [k for k, v in self.systems_enabled.items() if v],
                "generated_at": datetime.utcnow().isoformat(),
                "quality_score": self._calculate_quality_score(final_analysis),
                "data_sources_used": len(research_data.get("sources", [])),
                "ai_models_used": 1 if self.systems_enabled['gemini'] else 0
            }
            
            logger.info(f"✅ Análise abrangente concluída em {processing_time:.2f} segundos")
            return final_analysis
            
        except Exception as e:
            logger.error(f"❌ Erro na análise abrangente: {str(e)}", exc_info=True)
            return self._generate_fallback_analysis(data, str(e))
    
    def _collect_research_data(
        self, 
        data: Dict[str, Any], 
        session_id: Optional[str]
    ) -> Dict[str, Any]:
        """Coleta dados de pesquisa de múltiplas fontes"""
        
        research_data = {
            "web_research": {},
            "deep_search": {},
            "sources": [],
            "total_content_length": 0
        }
        
        # 1. Pesquisa web com WebSailor
        if self.systems_enabled['websailor'] and data.get('query'):
            logger.info("🌐 Executando pesquisa web com WebSailor...")
            try:
                web_result = websailor_agent.navigate_and_research(
                    data['query'],
                    context={
                        "segmento": data.get('segmento'),
                        "produto": data.get('produto'),
                        "publico": data.get('publico')
                    },
                    max_pages=8,
                    depth=2,
                    aggressive_mode=True
                )
                research_data["web_research"] = web_result
                research_data["sources"].extend(web_result.get("sources", []))
                
                # Adiciona conteúdo combinado
                combined_content = web_result.get("research_summary", {}).get("combined_content", "")
                research_data["total_content_length"] += len(combined_content)
                
                logger.info(f"✅ WebSailor: {len(web_result.get('sources', []))} fontes analisadas")
            except Exception as e:
                logger.error(f"Erro no WebSailor: {str(e)}")
        
        # 2. Deep Search
        if self.systems_enabled['deep_search'] and data.get('query'):
            logger.info("🔬 Executando deep search...")
            try:
                deep_result = deep_search_service.perform_deep_search(
                    data['query'],
                    data,
                    max_results=15
                )
                research_data["deep_search"] = deep_result
                research_data["total_content_length"] += len(str(deep_result))
                
                logger.info("✅ Deep search concluído")
            except Exception as e:
                logger.error(f"Erro no Deep Search: {str(e)}")
        
        return research_data
    
    def _perform_ai_analysis(
        self, 
        data: Dict[str, Any], 
        research_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Executa análise com IA usando Gemini"""
        
        if not self.systems_enabled['gemini']:
            logger.warning("Gemini não disponível - usando análise básica")
            return self._generate_basic_analysis(data)
        
        try:
            # Prepara contexto de pesquisa
            search_context = ""
            if research_data.get("web_research"):
                web_summary = research_data["web_research"].get("research_summary", {})
                search_context += f"PESQUISA WEB:\n{web_summary.get('combined_content', '')}\n\n"
                
                insights = web_summary.get("key_insights", [])
                if insights:
                    search_context += f"INSIGHTS WEB:\n" + "\n".join(insights) + "\n\n"
            
            if research_data.get("deep_search"):
                search_context += f"DEEP SEARCH:\n{research_data['deep_search']}\n\n"
            
            # Executa análise com Gemini
            logger.info("🤖 Executando análise com Gemini Pro...")
            gemini_result = gemini_client.generate_ultra_detailed_analysis(
                data,
                search_context=search_context[:15000] if search_context else None,
                attachments_context=None
            )
            
            logger.info("✅ Análise Gemini concluída")
            return gemini_result
            
        except Exception as e:
            logger.error(f"Erro na análise Gemini: {str(e)}")
            return self._generate_basic_analysis(data)
    
    def _consolidate_analysis(
        self, 
        data: Dict[str, Any], 
        research_data: Dict[str, Any], 
        ai_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Consolida toda a análise"""
        
        # Usa análise da IA como base
        consolidated = ai_analysis.copy()
        
        # Enriquece com dados de pesquisa
        if research_data.get("web_research"):
            consolidated["pesquisa_web_detalhada"] = research_data["web_research"]
        
        if research_data.get("deep_search"):
            consolidated["pesquisa_profunda"] = research_data["deep_search"]
        
        # Adiciona insights exclusivos baseados na pesquisa
        exclusive_insights = self._generate_exclusive_insights(data, research_data, ai_analysis)
        if exclusive_insights:
            existing_insights = consolidated.get("insights_exclusivos", [])
            consolidated["insights_exclusivos"] = existing_insights + exclusive_insights
        
        return consolidated
    
    def _generate_exclusive_insights(
        self, 
        data: Dict[str, Any], 
        research_data: Dict[str, Any], 
        ai_analysis: Dict[str, Any]
    ) -> List[str]:
        """Gera insights exclusivos baseados na pesquisa"""
        
        insights = []
        
        # Insights baseados na pesquisa web
        if research_data.get("web_research"):
            web_insights = research_data["web_research"].get("research_summary", {}).get("key_insights", [])
            for insight in web_insights[:3]:
                insights.append(f"🌐 Pesquisa Web: {insight}")
        
        # Insights baseados no deep search
        if research_data.get("deep_search"):
            insights.append(f"🔍 Deep Search: Análise profunda realizada com {len(research_data.get('sources', []))} fontes")
        
        # Insights sobre qualidade dos dados
        total_sources = len(research_data.get("sources", []))
        if total_sources > 0:
            insights.append(f"📊 Qualidade dos Dados: Análise baseada em {total_sources} fontes verificadas")
        
        return insights[:5]  # Máximo 5 insights exclusivos
    
    def _generate_basic_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera análise básica quando IA não está disponível"""
        
        return {
            "avatar_ultra_detalhado": {
                "perfil_demografico": {
                    "idade": "25-45 anos",
                    "renda": "R$ 3.000 - R$ 15.000",
                    "escolaridade": "Superior",
                    "localizacao": "Centros urbanos"
                },
                "dores_especificas": [
                    "Falta de conhecimento especializado",
                    "Dificuldade para implementar estratégias",
                    "Resultados inconsistentes",
                    "Falta de direcionamento claro"
                ],
                "desejos_profundos": [
                    "Alcançar liberdade financeira",
                    "Ter mais tempo para família",
                    "Ser reconhecido como especialista",
                    "Fazer diferença no mundo"
                ]
            },
            "escopo": {
                "posicionamento_mercado": "Solução premium para resultados rápidos",
                "proposta_valor": "Transforme seu negócio com estratégias comprovadas",
                "diferenciais_competitivos": ["Metodologia exclusiva", "Suporte personalizado"]
            },
            "estrategia_palavras_chave": {
                "palavras_primarias": [data.get('segmento', 'negócio'), "estratégia", "marketing"],
                "palavras_secundarias": ["crescimento", "vendas", "digital", "online"],
                "palavras_cauda_longa": [f"como crescer no {data.get('segmento', 'mercado')}", "estratégias de marketing digital"]
            },
            "insights_exclusivos": [
                f"O mercado de {data.get('segmento', 'negócios')} apresenta oportunidades de crescimento",
                "A digitalização é uma tendência irreversível no setor",
                "Investimento em marketing digital é essencial para competitividade",
                "Personalização da experiência do cliente é um diferencial competitivo",
                "Análise gerada em modo básico - configure as APIs para análise completa"
            ]
        }
    
    def _calculate_quality_score(self, analysis: Dict[str, Any]) -> float:
        """Calcula score de qualidade da análise"""
        
        score = 0.0
        max_score = 100.0
        
        # Pontuação por seções principais (60 pontos)
        main_sections = [
            "avatar_ultra_detalhado", "escopo", "estrategia_palavras_chave", "insights_exclusivos"
        ]
        
        for section in main_sections:
            if section in analysis and analysis[section]:
                score += 15.0  # 60/4 = 15 pontos por seção
        
        # Pontuação por pesquisa (20 pontos)
        if "pesquisa_web_detalhada" in analysis:
            score += 10.0
        if "pesquisa_profunda" in analysis:
            score += 10.0
        
        # Pontuação por insights (20 pontos)
        insights = analysis.get("insights_exclusivos", [])
        if len(insights) >= 5:
            score += 20.0
        elif len(insights) >= 3:
            score += 15.0
        elif len(insights) >= 1:
            score += 10.0
        
        return min(score, max_score)
    
    def _generate_fallback_analysis(self, data: Dict[str, Any], error: str) -> Dict[str, Any]:
        """Gera análise de emergência"""
        
        logger.error(f"Gerando análise de emergência devido a: {error}")
        
        basic_analysis = self._generate_basic_analysis(data)
        basic_analysis["insights_exclusivos"].append(f"⚠️ Erro no processamento: {error}")
        basic_analysis["insights_exclusivos"].append("🔄 Recomenda-se executar nova análise")
        
        basic_analysis["metadata"] = {
            "processing_time_seconds": 0,
            "analysis_engine": "Emergency Fallback",
            "generated_at": datetime.utcnow().isoformat(),
            "quality_score": 25.0,
            "error": error,
            "recommendation": "Execute nova análise com configuração completa"
        }
        
        return basic_analysis

# Instância global do motor
enhanced_analysis_engine = EnhancedAnalysisEngine()