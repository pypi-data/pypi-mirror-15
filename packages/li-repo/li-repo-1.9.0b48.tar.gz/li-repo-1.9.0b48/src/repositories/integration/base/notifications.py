# -*- coding: utf-8 -*-
import os
import json
from li_api_client.integration import ApiIntegration
from repositories.integration.models import (
    AccountIntegration, ModelIntegration, IntegrationHistory)


class BaseNotificationService(object):
    def __init__(
            self,
            instance,
            *args,
            **kwargs):
        super(BaseNotificationService, self).__init__(*args, **kwargs)
        self.instance = instance
        self.sandbox = os.environ.get('ENVIRONMENT') != 'production'
        if hasattr(instance, 'conta'):
            self.account_id = instance.conta.id
        else:
            self.account_id = args.pop('account', None)
        self.crud = '',
        self.integration_list = []
        self.model_dict = {}

    # Checar se os dados são válidos
    def validate_args(self):
        if not self.model:
            raise ValueError(u"É preciso definir o modelo usando nesta classe")
        elif self.model != self.instance._meta.model:
            raise ValueError(
                u"A instância enviada não é compativel com o modelo")
        if not self.account_id:
            raise ValueError("Informe a conta")

    # Se for sandbox, adicionar o produto as integracoes ativas
    def process_sandbox(self):
        active_integrations = AccountIntegration.objects.filter(active=True)
        for account_integration in active_integrations:
            new_model_integration, \
                created = ModelIntegration.objects.get_or_create(
                    account_id=self.account_id,
                    model_selected=self.model._meta.model_name,
                    model_selected_id=self.instance.id,
                    integration=account_integration.integration
                )

    def model_select_is_valid(self, obj):
        """
                Sobrescrever este método para validações
                específicas do modelo
        """
        return True

    # Listar conectores válidos para modelo/loja enviados
    def get_connectors(self):
        self.integration_list = [
            model_for_integration
            for model_for_integration in ModelIntegration.objects.filter(
                account_id=self.account_id,
                model_selected=self.model._meta.model_name,
                model_selected_id=self.instance.id,
            )
            if model_for_integration.active() and
            self.model_select_is_valid(
                model_for_integration.get_object(
                    self.model))
        ]
        return self.integration_list

    # Definir Create, Update, Delete (Removed) ou Delete (Model)
    def set_crud(self, crud=None):
        self.crud = crud

    # Gerar o dicionario
    def model_to_dict(self):
        """
        Sobrescrever esta classe passando a
        classe serializadora correspondente
        """
        raise NotImplementedError("Implementar serialização")

    # Enviar notificação
    def send_notification(self):
        # Uma mensagem para todos os conectores
        self.model_dict['connector_list'] = [
            model_integration.integration.slug
            for model_integration in self.integration_list
        ]
        for model_integration in self.integration_list:
            integration_history, \
                created = IntegrationHistory.objects.get_or_create(
                    account_id=self.account_id,
                    model_selected=self.instance._meta.model_name,
                    model_selected_id=self.instance.pk,
                    integration=model_integration.integration,
                    message_body=json.dumps(self.model_dict),
                    status="WAIT"
                )
            print("CRIOU HISTORICO: {}".format(integration_history.id))

    def use_internal_api(self):
        history_list = IntegrationHistory.objects.filter(
            account_id=self.account_id,
            status="WAIT"
        )
        for history in history_list:
            # Criar a notificação via API interna
            ApiIntegration().send_notification(
                crud=self.crud,
                history_id=history.id,
                model_dict=json.dumps(self.model_dict)
            )

    # Processar Notificacao
    def notify(self, crud):
        self.validate_args()
        if self.sandbox:
            self.process_sandbox()
        self.get_connectors()
        if self.integration_list:
            self.set_crud(crud)
            self.model_to_dict()
            self.send_notification()
            self.use_internal_api()
