import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { 
  Train, 
  Bus, 
  Clock, 
  Users, 
  AlertCircle, 
  CheckCircle,
  RefreshCw,
  MapPin
} from 'lucide-react'

const RealtimeStatus = ({ line, onRefresh }) => {
  const [lineStatus, setLineStatus] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchLineStatus()
  }, [line.id])

  const fetchLineStatus = async () => {
    setLoading(true)
    try {
      const response = await fetch(`/api/status/realtime/${line.id}`)
      if (response.ok) {
        const data = await response.json()
        setLineStatus(data)
      }
    } catch (error) {
      console.error('Erro ao carregar status da linha:', error)
    } finally {
      setLoading(false)
    }
  }

  const getLineIcon = (lineType) => {
    switch (lineType) {
      case 'metro':
      case 'trem':
        return <Train className="h-5 w-5" />
      case 'onibus':
        return <Bus className="h-5 w-5" />
      default:
        return <Train className="h-5 w-5" />
    }
  }

  const getStatusIcon = (statusType) => {
    switch (statusType) {
      case 'esperando':
        return <Clock className="h-4 w-4" />
      case 'embarcado':
        return <CheckCircle className="h-4 w-4" />
      case 'cheio':
        return <Users className="h-4 w-4" />
      case 'parado':
        return <AlertCircle className="h-4 w-4" />
      case 'andando':
        return <CheckCircle className="h-4 w-4" />
      default:
        return <MapPin className="h-4 w-4" />
    }
  }

  const getStatusColor = (statusType) => {
    switch (statusType) {
      case 'esperando':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      case 'embarcado':
        return 'bg-green-100 text-green-800 border-green-200'
      case 'cheio':
        return 'bg-red-100 text-red-800 border-red-200'
      case 'parado':
        return 'bg-red-100 text-red-800 border-red-200'
      case 'andando':
        return 'bg-green-100 text-green-800 border-green-200'
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  const formatTime = (timestamp) => {
    const now = new Date()
    const reportTime = new Date(timestamp)
    const diffMinutes = Math.floor((now - reportTime) / (1000 * 60))
    
    if (diffMinutes < 1) {
      return 'Agora mesmo'
    } else if (diffMinutes < 60) {
      return `${diffMinutes} min atrás`
    } else {
      return reportTime.toLocaleTimeString('pt-BR', {
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }

  const getOverallStatus = () => {
    if (!lineStatus || !lineStatus.recent_reports || lineStatus.recent_reports.length === 0) {
      return { status: 'sem-dados', label: 'Sem dados', color: 'bg-gray-100 text-gray-800' }
    }

    const recentReports = lineStatus.recent_reports.slice(0, 5)
    const statusCounts = {}
    
    recentReports.forEach(report => {
      statusCounts[report.status_type] = (statusCounts[report.status_type] || 0) + 1
    })

    // Prioridade: parado > cheio > esperando > embarcado/andando
    if (statusCounts.parado > 0) {
      return { status: 'parado', label: 'Problemas reportados', color: 'bg-red-100 text-red-800' }
    } else if (statusCounts.cheio > 0) {
      return { status: 'cheio', label: 'Veículos cheios', color: 'bg-orange-100 text-orange-800' }
    } else if (statusCounts.esperando > 0) {
      return { status: 'esperando', label: 'Usuários aguardando', color: 'bg-yellow-100 text-yellow-800' }
    } else {
      return { status: 'normal', label: 'Funcionamento normal', color: 'bg-green-100 text-green-800' }
    }
  }

  const overallStatus = getOverallStatus()

  return (
    <Card className="h-full">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            {getLineIcon(line.type)}
            <div>
              <CardTitle className="text-lg">{line.name}</CardTitle>
              <CardDescription className="capitalize">{line.type}</CardDescription>
            </div>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={fetchLineStatus}
            disabled={loading}
          >
            <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
          </Button>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-4">
        {/* Status Geral */}
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium">Status Geral:</span>
          <Badge className={overallStatus.color}>
            {overallStatus.label}
          </Badge>
        </div>

        {/* Relatórios Recentes */}
        {lineStatus && lineStatus.recent_reports && lineStatus.recent_reports.length > 0 ? (
          <div className="space-y-3">
            <h4 className="text-sm font-medium text-gray-700">Últimos Relatórios:</h4>
            <div className="space-y-2">
              {lineStatus.recent_reports.slice(0, 3).map((report) => (
                <div key={report.id} className="flex items-center justify-between p-2 bg-gray-50 rounded-md">
                  <div className="flex items-center space-x-2">
                    <Badge variant="outline" className={getStatusColor(report.status_type)}>
                      <div className="flex items-center space-x-1">
                        {getStatusIcon(report.status_type)}
                        <span className="text-xs">{report.status_type}</span>
                      </div>
                    </Badge>
                    {report.station && (
                      <span className="text-xs text-gray-600">{report.station.name}</span>
                    )}
                  </div>
                  <span className="text-xs text-gray-500">
                    {formatTime(report.timestamp)}
                  </span>
                </div>
              ))}
            </div>
            
            {report.message && (
              <div className="mt-2 p-2 bg-blue-50 rounded-md">
                <p className="text-xs text-blue-800">"{report.message}"</p>
              </div>
            )}
          </div>
        ) : (
          <div className="text-center py-6">
            <MapPin className="h-8 w-8 text-gray-400 mx-auto mb-2" />
            <p className="text-sm text-gray-500">
              Nenhum relatório recente
            </p>
            <p className="text-xs text-gray-400">
              Seja o primeiro a reportar o status!
            </p>
          </div>
        )}

        {/* Estatísticas */}
        {lineStatus && lineStatus.recent_reports && lineStatus.recent_reports.length > 0 && (
          <div className="pt-3 border-t">
            <div className="flex justify-between text-xs text-gray-600">
              <span>Total de relatórios:</span>
              <span className="font-medium">{lineStatus.recent_reports.length}</span>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  )
}

export default RealtimeStatus

