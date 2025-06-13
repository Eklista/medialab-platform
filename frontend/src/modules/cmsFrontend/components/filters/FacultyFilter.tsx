// frontend/src/modules/cmsFrontend/components/filters/FacultyFilter.tsx
import React, { useState } from 'react';
import { ChevronDown, ChevronRight, GraduationCap, Calendar, Camera } from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';

// Mock data - esto vendrá del backend
const mockFaculties = [
  {
    id: 1,
    name: 'FISICC',
    fullName: 'Facultad de Ingeniería de Sistemas',
    categories: [
      { id: 1, name: 'Graduaciones', count: 12, icon: GraduationCap },
      { id: 2, name: 'Conferencias', count: 8, icon: Calendar },
      { id: 3, name: 'Eventos', count: 15, icon: Camera },
    ]
  },
  {
    id: 2,
    name: 'FING',
    fullName: 'Facultad de Ingeniería',
    categories: [
      { id: 4, name: 'Graduaciones', count: 18, icon: GraduationCap },
      { id: 5, name: 'Talleres', count: 6, icon: Calendar },
    ]
  },
  {
    id: 3,
    name: 'FACMED',
    fullName: 'Facultad de Medicina',
    categories: [
      { id: 6, name: 'Graduaciones', count: 25, icon: GraduationCap },
      { id: 7, name: 'Simposiums', count: 4, icon: Calendar },
      { id: 8, name: 'Prácticas', count: 9, icon: Camera },
    ]
  }
];

export const FacultyFilter: React.FC = () => {
  const { isDark } = useTheme();
  const [expandedFaculties, setExpandedFaculties] = useState<number[]>([1]);
  const [selectedCategory, setSelectedCategory] = useState<number | null>(null);

  const toggleFaculty = (facultyId: number) => {
    setExpandedFaculties(prev => 
      prev.includes(facultyId) 
        ? prev.filter(id => id !== facultyId)
        : [...prev, facultyId]
    );
  };

  return (
    <div className="space-y-2">
      {mockFaculties.map(faculty => (
        <div key={faculty.id} className="space-y-1">
          {/* Faculty Header */}
          <button
            onClick={() => toggleFaculty(faculty.id)}
            className={`w-full flex items-center gap-2 px-3 py-2 rounded-lg text-left transition-colors ${
              isDark
                ? 'hover:bg-slate-700 text-slate-200'
                : 'hover:bg-slate-100 text-slate-700'
            }`}
          >
            {expandedFaculties.includes(faculty.id) ? (
              <ChevronDown className="w-4 h-4 flex-shrink-0" />
            ) : (
              <ChevronRight className="w-4 h-4 flex-shrink-0" />
            )}
            
            <div className="flex-1 min-w-0">
              <div className={`font-medium text-sm ${
                isDark ? 'text-slate-100' : 'text-slate-900'
              }`}>
                {faculty.name}
              </div>
              <div className={`text-xs truncate ${
                isDark ? 'text-slate-400' : 'text-slate-500'
              }`}>
                {faculty.fullName}
              </div>
            </div>
          </button>

          {/* Categories */}
          {expandedFaculties.includes(faculty.id) && (
            <div className="ml-6 space-y-1">
              {faculty.categories.map(category => {
                const Icon = category.icon;
                const isSelected = selectedCategory === category.id;
                
                return (
                  <button
                    key={category.id}
                    onClick={() => setSelectedCategory(isSelected ? null : category.id)}
                    className={`w-full flex items-center gap-2 px-3 py-2 rounded-lg text-left transition-colors ${
                      isSelected
                        ? isDark
                          ? 'bg-blue-600 text-white'
                          : 'bg-blue-600 text-white'
                        : isDark
                          ? 'hover:bg-slate-700 text-slate-300'
                          : 'hover:bg-slate-100 text-slate-600'
                    }`}
                  >
                    <Icon className="w-4 h-4 flex-shrink-0" />
                    <span className="flex-1 text-sm font-medium">
                      {category.name}
                    </span>
                    <span className={`text-xs px-2 py-0.5 rounded-full ${
                      isSelected
                        ? 'bg-white/20 text-white'
                        : isDark
                          ? 'bg-slate-600 text-slate-300'
                          : 'bg-slate-200 text-slate-600'
                    }`}>
                      {category.count}
                    </span>
                  </button>
                );
              })}
            </div>
          )}
        </div>
      ))}
    </div>
  );
};
